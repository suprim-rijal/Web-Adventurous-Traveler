
let map;
let markers = {};
let currentGameId = null;
let gameState = {};
let playerName = '';
let L = window.L;


document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    currentGameId = urlParams.get('game_id') || getCookie('game_id');
    
    if (!currentGameId) {
        window.location.href = '/welcome';
        return;
    }
    

    const quitBtn = document.createElement('button');
    quitBtn.className = 'quit-button';
    quitBtn.innerHTML = '<i class="fas fa-sign-out-alt"></i> Quit Game';
    quitBtn.onclick = showQuitConfirmation;
    document.querySelector('.game-header').appendChild(quitBtn);
    
    initializeMap();
    loadGameState();
    setupEventListeners();
});

// Map loading
function initializeMap() {
    map = L.map('map').setView([48.0, 10.0], 4);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 12,
        minZoom: 3
    }).addTo(map);
}

// Load game state from server
function loadGameState() {
    showLoading(true);
    
    fetch(`/api/game/state?game_id=${currentGameId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                showMessage('error', data.error);
                setTimeout(() => window.location.href = '/welcome', 2000);
                return;
            }
            
            gameState = data;
            updateUI(data);
            updateMapMarkers(data);
            showLoading(false);
            
            if (data.game_status === 'WON') {
                showWinScreen(data);
            } else if (data.game_status === 'LOST' || data.game_status === 'QUIT') {
                showLoseScreen(data);
            }
        })
        .catch(error => {
            console.error('Error loading game state:', error);
            showMessage('error', 'Failed to load game. Please try again.');
            showLoading(false);
        });
}

// Update UI with game state
function updateUI(data) {
    const game = data.game;
    playerName = game.player_name;
    
    
    document.getElementById('player-name').textContent = playerName;
    document.getElementById('money-display').textContent = `$${game.money}`;
    document.getElementById('fuel-display').textContent = `${game.fuel_km}km`;
    document.getElementById('location-display').textContent = game.current_airport_code || '-';
    document.getElementById('artifacts-display').textContent = `${game.artifacts_delivered}/10`;
    document.getElementById('travels-display').textContent = game.travels_remaining;
    
   
    updateMissionOverlay(game);
    updateLogsTab(data.logs);
    updateQuestsTab(data.quests);
    updateCluesTab(data.clues);
    updateProgressTab(data);
    
    updateShopModal();
    updateArtifactsModal(data.player_artifacts);
    updateCluesModal(data.clues);
    updateStatusModal(game);
}

function updateMissionOverlay(game) {
    const missionOverlay = document.getElementById('mission-overlay');
    const phaseIndicator = document.getElementById('phase-indicator');
    const missionText = document.getElementById('mission-text');
    const artifactProgress = document.getElementById('artifact-progress-info');
    
    if (game.current_phase === 'FINDING_ARTIFACTS') {
        phaseIndicator.innerHTML = '<div class="phase-badge phase-finding">Finding Artifacts</div>';
        if (game.artifact_airport_code) {
            missionText.textContent = `You're at the artifact airport (${game.artifact_airport_code})! Dig to find artifacts.`;
        } else {
            missionText.textContent = 'Find the airport where all 10 artifacts are hidden. Use clues to locate it.';
        }
        
        artifactProgress.innerHTML = `
            <div style="margin-top: 10px; font-size: 0.9rem; color: #7f8c8d;">
                <i class="fas fa-search"></i> Search for the hidden artifact airport
            </div>
        `;
    } else {
        phaseIndicator.innerHTML = '<div class="phase-badge phase-delivering">Delivering Artifacts</div>';
        missionText.textContent = `Deliver artifacts to their destinations. ${game.artifacts_delivered}/10 delivered.`;
        
        artifactProgress.innerHTML = `
            <div style="margin-top: 10px; font-size: 0.9rem; color: #f39c12;">
                <i class="fas fa-gem"></i> ${10 - game.artifacts_delivered} artifacts to deliver
            </div>
        `;
    }
}

function updateMapMarkers(data) {
    Object.values(markers).forEach(marker => marker.remove());
    markers = {};
    const game = data.game;
    const airports = data.airports;
    
    airports.forEach(airport => {
        let markerColor = '#3498db';
        let markerClass = 'marker-neutral';
        
        if (airport.id === game.current_airport_id) {
            markerColor = '#e74c3c';
            markerClass = 'marker-current';
        }
        else if (data.logs?.some(log => log.airport_id === airport.id && log.log_type === 'FLIGHT')) {
            markerColor = '#2ecc71';
            markerClass = 'marker-visited';
        }
        const exactClues = data.clues?.filter(clue => 
            clue.target_airport_id === airport.id && 
            clue.clue_type === 'EXACT_LOCATION'
        ) || [];
        
        if (exactClues.length > 0) {
            markerColor = '#9b59b6';
            markerClass = 'marker-revealed';
        }
        const marker = L.circleMarker([airport.latitude, airport.longitude], {
            radius: 8,
            fillColor: markerColor,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8,
            className: `map-marker ${markerClass}`
        }).addTo(map);
        
        markers[airport.id] = marker;
        const popupContent = createPopupContent(airport, game, data, exactClues);
        marker.bindPopup(popupContent, {
            className: 'airport-popup',
            maxWidth: 300
        });
    });
    
    if (airports.length > 0) {
        const bounds = L.latLngBounds(airports.map(a => [a.latitude, a.longitude]));
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

function createPopupContent(airport, game, data, exactClues) {
    const isCurrent = airport.id === game.current_airport_id;
    const distance = isCurrent ? 0 : calculateDistance(
        game.current_latitude, game.current_longitude,
        airport.latitude, airport.longitude
    );
    const fuelCost = Math.floor(distance * 0.9);
    const hasFuelPass = game.fuel_pass_remaining > 0;
    const canTravel = (hasFuelPass || game.fuel_km >= fuelCost) && game.travels_remaining > 0 && !isCurrent;
    let content = `
        <h4>${airport.name} (${airport.code})</h4>
        <div class="popup-info">
            <div><strong>Location:</strong> ${airport.city}, ${airport.country}</div>
            <div><strong>Region:</strong> ${airport.region}</div>
            <div><strong>Type:</strong> ${airport.airport_size} airport</div>
            <div><strong>Runway:</strong> ${airport.runway_length_m}m</div>
            ${airport.is_tourist_destination ? '<div><i class="fas fa-camera"></i> Tourist Destination</div>' : ''}
        </div>
    `;
    
    if (isCurrent) {
        content += '<div class="current-badge"><i class="fas fa-plane"></i> CURRENT LOCATION</div>';
        if (game.current_phase === 'FINDING_ARTIFACTS' && airport.id === game.artifact_airport_id) {
            content += `
                <div style="margin: 10px 0; padding: 8px; background: #fff9e6; border-radius: 5px;">
                    <strong><i class="fas fa-digging"></i> Artifact Airport</strong><br>
                    <button class="popup-btn action-btn-popup" onclick="digForArtifacts()" style="margin-top: 8px;">
                        <i class="fas fa-shovel"></i> Dig for Artifacts
                    </button>
                </div>
            `;
        }
        if (game.current_phase === 'DELIVERING_ARTIFACTS') {
            const artifactsHere = data.player_artifacts?.filter(a => 
                a.delivery_airport_id === airport.id && a.status === 'FOUND'
            ) || [];
            
            if (artifactsHere.length > 0) {
                content += `
                    <div style="margin: 10px 0; padding: 8px; background: #e8f6f3; border-radius: 5px;">
                        <strong><i class="fas fa-gift"></i> Delivery Location</strong><br>
                        ${artifactsHere.length} artifact${artifactsHere.length > 1 ? 's' : ''} to deliver
                        <button class="popup-btn action-btn-popup" onclick="deliverArtifacts()" style="margin-top: 8px;">
                            <i class="fas fa-truck"></i> Deliver Artifacts
                        </button>
                    </div>
                `;
            }
        }
    }
    if (exactClues.length > 0) {
        content += '<div style="margin: 10px 0; padding: 8px; background: #f3e5f5; border-radius: 5px; border-left: 3px solid #9b59b6;">';
        content += '<strong><i class="fas fa-map-marker-alt"></i> Revealed Location:</strong><br>';
        exactClues.forEach(clue => {
            content += `<div style="margin-top: 5px; font-size: 0.9em;">${clue.clue_text}</div>`;
        });
        content += '</div>';
    }
    
    content += '<div class="popup-actions">';
    
    if (!isCurrent) {
        let travelBtnText = 'Travel Here';
        let fuelInfo = '';
        
        if (hasFuelPass) {
            travelBtnText = 'Travel Here (Fuel Pass)';
            fuelInfo = `<span style="font-size: 0.8em; margin-left: auto; color: #2ecc71;">
                <i class="fas fa-ticket-alt"></i> ${distance}km (FREE - ${game.fuel_pass_remaining} passes left)
            </span>`;
        } else {
            fuelInfo = `<span style="font-size: 0.8em; margin-left: auto;">
                ${distance}km (${fuelCost}km fuel)
            </span>`;
        }
        
        content += `
            <button class="popup-btn travel-btn ${!canTravel ? 'disabled' : ''}" 
                    onclick="travelToAirport(${airport.id})"
                    ${!canTravel ? 'disabled' : ''}>
                <i class="fas fa-plane"></i>
                ${travelBtnText}
                ${fuelInfo}
            </button>
        `;
    }
    
    content += '</div>';
    return content;
}

function travelToAirport(destinationId) {
    showLoading(true);
    
    fetch('/api/game/travel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId,
            destination_airport_id: destinationId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            showMessage('error', data.error);
            showLoading(false);
            return;
        }

        let travelMsg = `Traveled to ${data.destination.code} (${data.distance}km)`;
        if (data.used_fuel_pass) {
            travelMsg += ' - FUEL PASS USED! (0km fuel cost)';
        } else {
            travelMsg += `, used ${data.fuel_cost}km fuel`;
        }
        showMessage('success', travelMsg);
        
        // Handle events
        if (data.event) {
            const eventType = data.event.type === 'POSITIVE' ? 'success' : 'error';
            showMessage(eventType, `${data.event.name}: ${data.event.description} ($${data.event.money_change}, ${data.event.fuel_change}km fuel)`);
        }
        // Handle clues
        if (data.clue) {
            showMessage('warning', `Clue Found: ${data.clue.text}`);
        }
        // Handle quests
        if (data.quest) {
            showMessage('info', `New Quest: ${data.quest.title} - ${data.quest.description}`);
        }
        // Check if at artifact airport
        if (data.at_artifact_airport) {
            showMessage('info', 'You found the artifact airport! Dig to find the artifacts.');
        }
        // Check if at delivery location
        if (data.can_deliver) {
            showMessage('info', `You can deliver ${data.artifacts_count} artifact(s) here.`);
        }
        // Reload game state
        setTimeout(() => {
            loadGameState();
        }, 1000);
    })
    .catch(error => {
        console.error('Error traveling:', error);
        showMessage('error', 'Failed to travel. Please try again.');
        showLoading(false);
    });
}
// Dig for artifacts
function digForArtifacts() {
    if (!confirm('Dig for artifacts at this airport?')) return;
    
    showLoading(true);
    
    fetch('/api/game/dig', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId
        })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (!data.success) {
            showMessage('error', data.error);
            return;
        }
        
        if (data.found) {
            showMessage('success', data.message);
            loadGameState();
        } else {
            showMessage('warning', data.message);
        }
    })
    .catch(error => {
        console.error('Error digging:', error);
        showMessage('error', 'Failed to dig for artifacts');
        showLoading(false);
    });
}

// Deliver artifacts
function deliverArtifacts() {
    if (!confirm('Deliver artifacts at this location?')) return;
    
    showLoading(true);
    
    fetch('/api/game/deliver', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId
        })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (!data.success) {
            showMessage('error', data.error);
            return;
        }
        
        showMessage('success', `Delivered ${data.delivered} artifact(s)! Earned $${data.money} and ${data.fuel}km fuel.`);
        loadGameState();
    })
    .catch(error => {
        console.error('Error delivering:', error);
        showMessage('error', 'Failed to deliver artifacts');
        showLoading(false);
    });
}

// Complete quest
function completeQuest(questId) {
    if (!confirm('Complete this quest?')) return;
    
    showLoading(true);
    
    fetch('/api/game/complete-quest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId,
            quest_id: questId
        })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (!data.success) {
            showMessage('error', data.error);
            return;
        }
        
        showMessage('success', `Quest completed! Rewards: $${data.quest.rewards.money}, ${data.quest.rewards.fuel}km fuel`);
        
        if (data.clue) {
            showMessage('warning', `Bonus Clue: ${data.clue.text}`);
        }
        
        loadGameState();
    })
    .catch(error => {
        console.error('Error completing quest:', error);
        showMessage('error', 'Failed to complete quest');
        showLoading(false);
    });
}

// Buy shop item
function buyShopItem(itemId) {
    showLoading(true);
    
    fetch('/api/shop/buy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId,
            item_id: itemId
        })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (!data.success) {
            showMessage('error', data.error);
            return;
        }
        
        showMessage('success', `Purchased ${data.item.name}!`);
        
        // Handle special results
        if (data.clue) {
            showMessage('warning', `Clue Revealed: ${data.clue.text}`);
        }
        
        
        loadGameState();
        closeModal('shop-modal');
    })
    .catch(error => {
        console.error('Error buying item:', error);
        showMessage('error', 'Failed to purchase item');
        showLoading(false);
    });
}


function showQuitConfirmation() {
    if (confirm('Are you sure you want to quit the game? Your progress will be saved.')) {
        quitGame();
    }
}

function quitGame() {
    showLoading(true);
    
    fetch('/api/game/quit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId
        })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.success) {
            showMessage('success', 'Game quit successfully');
            setTimeout(() => {
                window.location.href = '/welcome';
            }, 1500);
        } else {
            showMessage('error', data.error);
        }
    })
    .catch(error => {
        console.error('Error quitting game:', error);
        showMessage('error', 'Failed to quit game');
        showLoading(false);
    });
}

function updateLogsTab(logs) {
    const container = document.getElementById('events-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!logs || logs.length === 0) {
        container.innerHTML = '<div class="log-item"><div class="log-text">No logs yet.</div></div>';
        return;
    }
    const recentLogs = logs.slice(0, 5);
    recentLogs.forEach(log => {
        const logElement = document.createElement('div');
        logElement.className = 'log-item';
        logElement.innerHTML = `
            <div class="log-text">${log.description}</div>
        `;
        container.appendChild(logElement);
    });
    updateFullLogsModal(logs);
}

function updateQuestsTab(quests) {
    const container = document.getElementById('quests-container');
    if (!container) return;
    container.innerHTML = '';
    if (!quests || quests.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; color: #95a5a6; padding: 20px;">
                <i class="fas fa-quest" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>No active quests. Complete flights to get new quests.</p>
            </div>
        `;
        return;
    }
    
    quests.forEach(quest => {
        const questElement = document.createElement('div');
        questElement.className = 'quest-item';
        
        const requirements = JSON.parse(quest.requirements || '{}');
        let progressText = '';
        
        if (quest.quest_type === 'EXPLORATION') {
            progressText = `Visit ${requirements.current_count || 0}/${requirements.regions_to_visit || 3} regions`;
        } else if (quest.quest_type === 'TRANSPORT') {
            progressText = `Travel ${requirements.current_km || 0}/${requirements.distance_km || 1000}km`;
        }
        
        questElement.innerHTML = `
            <div class="quest-header">
                <div class="quest-title">${quest.title}</div>
            </div>
            <div class="quest-description">${quest.description}</div>
            ${progressText ? `<div style="font-size: 0.85rem; color: #f39c12; margin: 8px 0;"><i class="fas fa-chart-line"></i> ${progressText}</div>` : ''}
            <div class="quest-footer">
                <div class="quest-reward">
                    <span><i class="fas fa-money-bill-wave"></i> $${quest.reward_money}</span>
                    <span><i class="fas fa-gas-pump"></i> ${quest.reward_fuel}km</span>
                </div>
                <button class="complete-quest-btn" onclick="completeQuest(${quest.id})" id="quest-btn-${quest.id}">
                    Complete
                </button>
            </div>
        `;
        container.appendChild(questElement);
    });
}

function updateCluesTab(clues) {
    const container = document.getElementById('clues-container');
    if (!container) return;
    container.innerHTML = '';
    if (!clues || clues.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; color: #95a5a6; padding: 20px;">
                <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 10px;"></i>
                <p>No clues discovered yet. Fly to discover clues!</p>
            </div>
        `;
        return;
    }
    const recentClues = clues.slice(0, 3);
    recentClues.forEach(clue => {
        const clueElement = document.createElement('div');
        clueElement.className = 'clue-item';
        
        clueElement.innerHTML = `
            <div class="clue-text">${clue.clue_text}</div>
        `;
        container.appendChild(clueElement);
    });
}

function updateProgressTab(data) {
    const game = data.game;
    const foundCount = game.artifacts_found || 0;
    const deliveredCount = game.artifacts_delivered || 0;
    const artifactProgress = (deliveredCount / 10) * 100;
    
    document.getElementById('artifact-progress-bar').style.width = `${artifactProgress}%`;
    document.getElementById('artifact-found-count').textContent = `${foundCount} found`;
    document.getElementById('artifact-delivered-count').textContent = `${deliveredCount} delivered`;
    
    // Travel progress
    const travelsUsed = game.travels_used || 0;
    const travelsLeft = game.travels_remaining || 0;
    const travelProgress = (travelsUsed / 20) * 100;
    
    document.getElementById('travel-progress-bar').style.width = `${travelProgress}%`;
    document.getElementById('travels-used-count').textContent = `${travelsUsed} used`;
    document.getElementById('travels-left-count').textContent = `${travelsLeft} left`;
    
    // Current resources
    document.getElementById('current-fuel').textContent = `${game.fuel_km}km`;
    document.getElementById('current-money').textContent = `$${game.money}`;
}
function updateShopModal() {
    const container = document.getElementById('shop-items-container');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Loading shop items...</div>';
    
    fetch(`/api/shop/items?game_id=${currentGameId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
                return;
            }
            container.innerHTML = '';
            data.items.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.className = 'shop-item';
                
                itemElement.innerHTML = `
                    <div class="shop-item-header">
                        <div class="shop-item-title">${item.name}</div>
                        <div class="shop-item-price">$${item.price}</div>
                    </div>
                    <div class="shop-item-desc">${item.description}</div>
                    <div class="shop-item-details">
                        <i class="fas fa-${getItemIcon(item.category)}"></i> ${item.category} • 
                        ${item.purchased_count || 0}/${item.max_purchases_per_game || 3} purchased
                    </div>
                    <button class="buy-btn ${!item.can_purchase ? 'disabled' : ''}" 
                            onclick="buyShopItem(${item.id})"
                            ${!item.can_purchase ? 'disabled' : ''}>
                        ${!item.can_purchase ? 'Limit Reached' : 'Buy Now'}
                    </button>
                `;
                container.appendChild(itemElement);
            });
        })
        .catch(error => {
            console.error('Error loading shop:', error);
            container.innerHTML = '<div class="error">Failed to load shop items</div>';
        });
}

function updateArtifactsModal(artifacts) {
    const container = document.getElementById('artifacts-grid');
    if (!container || !artifacts) return;
    container.innerHTML = '';
    artifacts.forEach(artifact => {
        const card = document.createElement('div');
        card.className = `artifact-card ${artifact.status.toLowerCase()}`;
        
        let statusClass = 'status-hidden';
        let statusText = 'Hidden';
        let locationInfo = '';
        
        if (artifact.status === 'FOUND') {
            statusClass = 'status-found';
            statusText = 'Found';
            locationInfo = `<div style="font-size: 0.85rem; margin: 5px 0;"><i class="fas fa-map-marker-alt"></i> Deliver to ${artifact.delivery_airport_code || 'Unknown'}</div>`;
        } 
        
        card.innerHTML = `
            <div class="artifact-header">
                <div class="artifact-name">${artifact.artifact_name}</div>
                <div class="artifact-order">#${artifact.artifact_order}</div>
            </div>
            <div class="artifact-desc">${artifact.description}</div>
            
            
            <div class="artifact-reward">
                <span><i class="fas fa-money-bill-wave"></i> $${artifact.delivery_reward_money || 0}</span>
                <span><i class="fas fa-gas-pump"></i> ${artifact.delivery_reward_fuel || 0}km</span>
            </div>
        `;
        
        container.appendChild(card);
    });
}

function updateCluesModal(clues) {
    const container = document.getElementById('clues-container-modal');
    if (!container) return;
    
    if (!clues || clues.length === 0) {
        container.innerHTML = '<div class="loading">No clues discovered yet.</div>';
        return;
    }
    container.innerHTML = '';
    clues.forEach(clue => {
        const clueElement = document.createElement('div');
        clueElement.className = 'clue-item';
        clueElement.style.marginBottom = '15px';
        
        const time = new Date(clue.discovered_at).toLocaleString();
        
        clueElement.innerHTML = `
            <div class="clue-header">
                <div class="clue-artifact">${clue.artifact_name}</div>
            </div>
            <div class="clue-text">${clue.clue_text}</div>
        `;
        container.appendChild(clueElement);
    });
}
function updateStatusModal(game) {
    const container = document.getElementById('status-grid');
    if (!container) return;
    
    container.innerHTML = '';
    
    const stats = [
        { title: 'Player Name', value: game.player_name },
        { title: 'Current Location', value: `${game.current_airport_code} - ${game.current_city}, ${game.current_country}` },
        { title: 'Money', value: `$${game.money}` },
        { title: 'Fuel', value: `${game.fuel_km}km / ${game.max_fuel_capacity}km` },
        { title: 'Fuel Passes', value: game.fuel_pass_remaining || 0 }, // ADDED
        { title: 'Travels Used', value: `${game.travels_used} / (${game.travels_remaining} left)` }, // UPDATED
        { title: 'Travels Left', value: game.travels_remaining },
        { title: 'Artifacts Found', value: `${game.artifacts_found || 0} / 10` },
        { title: 'Artifacts Delivered', value: `${game.artifacts_delivered} / 10` },
        { title: 'Game Phase', value: game.current_phase.replace('_', ' ') },
        { title: 'Clue Accuracy Bonus', value: `${game.clue_accuracy_bonus || 0}%` },
        { title: 'Clue Reveal Chance', value: `${Math.round((0.40 + (game.clue_reveal_chance || 0)) * 100)}%` },
    ];
    
    stats.forEach(stat => {
        const statElement = document.createElement('div');
        statElement.className = 'status-item';
        
        statElement.innerHTML = `
            <h4>${stat.title}</h4>
            <div class="status-value">${stat.value}</div>
        `;
        
        container.appendChild(statElement);
    });
}
function updateFullLogsModal(logs) {
    const container = document.getElementById('full-events-list');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!logs || logs.length === 0) {
        container.innerHTML = '<div class="loading">No logs yet.</div>';
        return;
    }
    
    logs.forEach(log => {
        const logElement = document.createElement('div');
        logElement.className = 'log-item';
        logElement.style.marginBottom = '10px';
        
        logElement.innerHTML = `
            <div class="log-text">${log.description}</div>
        `;
        
        container.appendChild(logElement);
    });
}

function showWinScreen(data) {
    const game = data.game;
    
    document.getElementById('final-artifacts-delivered').textContent = `${game.artifacts_delivered}/10`;
    document.getElementById('final-travels-used').textContent = game.travels_used;
    document.getElementById('final-money').textContent = `$${game.money}`;
    document.getElementById('final-fuel').textContent = `${game.fuel_km}km`;
    
    const score = (game.artifacts_delivered * 1000) + (game.money) + (game.fuel_km * 2) + ((20 - game.travels_used) * 50);
    document.getElementById('final-score').textContent = score.toLocaleString();
    
    document.getElementById('game-screen').classList.remove('active');
    document.getElementById('win-screen').classList.add('active');
}

function showLoseScreen(data) {
    const game = data.game;
    
    document.getElementById('lose-reason').textContent = game.lose_reason || 'Mission failed';
    document.getElementById('lose-artifacts').textContent = `${game.artifacts_delivered}/10`;
    document.getElementById('lose-travels').textContent = game.travels_used;
    document.getElementById('lose-money').textContent = `$${game.money}`;
    document.getElementById('lose-fuel').textContent = `${game.fuel_km}km`;
    
    document.getElementById('game-screen').classList.remove('active');
    document.getElementById('lose-screen').classList.add('active');
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return Math.round(R * c);
}

function getQualityColor(quality) {
    switch(quality) {
        case 'low': return '#e74c3c';
        case 'medium': return '#f39c12';
        case 'high': return '#2ecc71';
        case 'exact': return '#9b59b6';
        default: return '#3498db';
    }
}

function getItemIcon(category) {
    switch(category) {
        case 'TRAVEL': return 'plane';
        case 'FUEL': return 'gas-pump';
        case 'UPGRADE': return 'wrench';
        case 'POWERUP': return 'bolt';
        case 'SERVICE': return 'concierge-bell';
        case 'LOOTBOX': return 'gift';
        default: return 'shopping-cart';
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showMessage(type, text) {
    const messageEl = document.getElementById('game-message');
    messageEl.textContent = text;
    messageEl.className = `message-${type}`;
    messageEl.style.display = 'block';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

function showLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    if (show) {
        spinner.classList.add('active');
    } else {
        spinner.classList.remove('active');
    }
}

function setupEventListeners() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById(`tab-${tab}`).classList.add('active');
        });
    });
    
    document.getElementById('sidebar-toggle').addEventListener('click', function() {
        const sidebar = document.getElementById('game-sidebar');
        const main = document.getElementById('main-container');
        const icon = this.querySelector('i');
        
        if (sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            main.classList.remove('sidebar-collapsed');
            icon.className = 'fas fa-chevron-left';
        } else {
            sidebar.classList.add('active');
            main.classList.add('sidebar-collapsed');
            icon.className = 'fas fa-chevron-right';
        }
    });
    
    document.getElementById('refresh-btn').addEventListener('click', function() {
        loadGameState();
        showMessage('info', 'Game state refreshed');
    });
    
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay').forEach(overlay => {
                overlay.classList.remove('active');
            });
        }
    });
}

