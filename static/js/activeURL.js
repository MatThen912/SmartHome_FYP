
$( document ).ready(function() {
    if (window.location.pathname.includes("home")) {
        $('#home').addClass('active');
    } else if (window.location.pathname.includes("faqs")) {
        $('#faqs').addClass('active');
    } else if (window.location.pathname.includes("dailyrecords")) {
        $('#dailyrecords').addClass('active');
        if (window.location.pathname.includes("mortalitiesList")) {
            $('#dailymortality').addClass('active');
        } else if (window.location.pathname.includes("feedusage")) {
            $('#dailyfeed').addClass('active');
        } else if (window.location.pathname.includes("medusage")) {
            $('#dailymed').addClass('active');
        } else if (window.location.pathname.includes("vacusage")) {
            $('#dailyvac').addClass('active');
        } 
    } else if (window.location.pathname.includes("")) {
        $('#').addClass('active');
    } else if (window.location.pathname.includes("stocksupplies")) {
        $('#stocksupplies').addClass('active');
    } else if (window.location.pathname.includes("balance")) {
        $('#balance').addClass('active');
    } else if (window.location.pathname.includes("chickshealth")) {
        $('#chickshealth').addClass('active');
    } else if (window.location.pathname.includes("customlogging")) {
        $('#customlogging').addClass('active');
    } else if (window.location.pathname.includes("downloads")) {
        $('#downloads').addClass('active');
    } 
});