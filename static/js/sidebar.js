  // click open/close dropdown for item registration
  function dropdownItemRegs() {
    var getItemRegsList = document.getElementById("itemRegs_list");
    var displaySetting = getItemRegsList.style.display;
    var getItemRegs = document.getElementById("itemRegs");
    if (displaySetting == 'block') {
        getItemRegs.style.color = "#67748e";
        getItemRegsList.style.display = 'none';
    } else {
        getItemRegs.style.color = "#5856D6";
        getItemRegsList.style.display = 'block';
    }
}

function dropdownResourceRegs() {
    var getItemRegsList = document.getElementById("resourceRegs_list");
    var displaySetting = getItemRegsList.style.display;
    var getItemRegs = document.getElementById("resourceRegs");
    if (displaySetting == 'block') {
        getItemRegs.style.color = "#67748e";
        getItemRegsList.style.display = 'none';
    } else {
        getItemRegs.style.color = "#5856D6";
        getItemRegsList.style.display = 'block';
    }
}

function dropdownDailyRecs() {
    var getItemRegsList = document.getElementById("DailyRecs_list");
    var displaySetting = getItemRegsList.style.display;
    var getItemRegs = document.getElementById("DailyRecs");
    if (displaySetting == 'block') {
        getItemRegs.style.color = "#67748e";
        getItemRegsList.style.display = 'none';
    } else {
        getItemRegs.style.color = "#5856D6";
        getItemRegsList.style.display = 'block';
    }
}

// function dropdownProfile() {
//     var getItemRegsList = document.getElementById("DailyRecs_list");
//     var displaySetting = getItemRegsList.style.display;
//     var getItemRegs = document.getElementById("DailyRecs");
//     if (displaySetting == 'block') {
//         getItemRegsList.style.display = 'none';
//     } else {
//         getItemRegsList.style.display = 'block';
//     }
// }