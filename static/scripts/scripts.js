

function addBadge(inputId, containerId) {
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
    const badges = $('.badge', container);
    badges.each(function() {
        badgeTexts.push($(this).text()); 
    });
    const string_badges = badgeTexts.join(",") 
    return string_badges;
}

function handleSubmit(event) {
    event.preventDefault();
    const fontesAp = document.getElementById('fontesAp');
    const areaAp = document.getElementById('areasAp');
    console.log(getBadgeText("selectedFontes"))
    console.log(getBadgeText("selectedAreas"))
    fontesAp.value = getBadgeText("selectedFontes");
    areaAp.value = getBadgeText("selectedAreas");
    event.target.form.submit();
}

