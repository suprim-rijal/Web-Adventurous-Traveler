
document.addEventListener('DOMContentLoaded', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            
            if (href && !href.startsWith('http') && !href.startsWith('#') && 
                href !== 'javascript:void(0)') {
                e.preventDefault();
                
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 500);
            }
        });
    });
    setActiveNavLink();
});

function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        const linkHref = link.getAttribute('href');

        if (linkHref && currentPath.includes(linkHref.replace('/', ''))) {
            link.classList.add('active');
        }

        if ((currentPath === '/' || currentPath.includes('index')) && 
            (linkHref === '/' || linkHref === '/index' || linkHref.includes('index'))) {
            link.classList.add('active');
        }
    });
}

function navigateTo(url) {
    document.body.style.opacity = '0';
    setTimeout(() => {
        window.location.href = url;
    }, 500);
}


window.addEventListener('pageshow', function(event) {
    
    if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
        document.body.style.opacity = '0';
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    }
});