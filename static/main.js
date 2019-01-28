

function change_inst1(value) {
    
    if (value) {
        window.inst1 = value;
    }
}

function change_inst2(value) {
    
    if (value) {
        window.inst2 = value;
    }
}
function change_major(value) {

    var info = getUrlVars();

    if (value) {
        window.major = value;
    }

    console.log(info.inst1)

    if (info.inst1 && info.inst2) { //enables changing major for same colleges
        window.inst1 = info.inst1;
        window.inst2 = info.inst2;
        submit();
    }
}

function submit() {
    var inst1 = window.inst1;
    var inst2 = window.inst2;
    var major = window.major;

    
    if (inst1 && inst2 && major) {
       window.location = '/?inst1=' + inst1 + '&inst2=' + inst2 + '&major=' + major;

    }
    else if (inst1 && inst2 ) {
       window.location = '/?inst1=' + inst1 + '&inst2=' + inst2; 
        
        
    }
    else {
        window.location = "/";   
    }

}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars;
}