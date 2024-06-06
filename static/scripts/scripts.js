

function addBadge(inputId, containerId) {
    console.log("This is running")
            const input = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const value = input.value.trim();

            if (value !== '') {
                const badge = document.createElement('span');
                badge.className = randomBadge();
                badge.textContent = value;
                container.appendChild(badge);
                input.value = '';

                badge.addEventListener('click', function () {
                    container.removeChild(badge);
                });
            }
        }


function randomBadge(){

    const classes = ["badge rounded-pill text-bg-primary","badge rounded-pill text-bg-success","badge rounded-pill text-bg-danger","badge rounded-pill text-bg-warning","badge rounded-pill text-bg-info","badge rounded-pill text-bg-dark"]
    const randomIndex = Math.floor(Math.random() * classes.length);
    return classes[randomIndex]
}


function getBadgeText(divId) {
    const container = document.getElementById(divId);
    const badgeTexts = [];
    const badges = container.querySelectorAll('.badge');
    badges.forEach(badge => {
        badgeTexts.push(badge.textContent);
    });
    const string_badges = badgeTexts.join(",") 
    return string_badges;
}

