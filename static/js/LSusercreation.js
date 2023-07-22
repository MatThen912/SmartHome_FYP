// patient form
document.getElementById("id_username").value = getSavedValue("id_username"); // set the value to this input
document.getElementById("id_dob").value = getSavedValue("id_dob"); // set the value to this input
document.getElementById("id_name").value = getSavedValue("id_name"); // set the value to this input
document.getElementById("id_email").value = getSavedValue("id_email"); // set the value to this input
document.getElementById("id_contact_number").value = getSavedValue("id_contact_number"); // set the value to this input
document.getElementById("id_ic_number").value = getSavedValue("id_ic_number"); // set the value to this input

//Save the value function - save it to localStorage as (ID, VALUE)
function saveValue(e){
    var id = e.id;  // get the sender's id to save it . 
    var val = e.value; // get the value. 
    localStorage.setItem(id, val);// Every time user writing something, the localStorage's value will override.
}

//get the saved value function - return the value of "v" from localStorage. 
function getSavedValue  (v){
    if (!localStorage.getItem(v)) {
        return "";// You can change this to your defualt value. 
    }
      return localStorage.getItem(v);
}

//clear form local storage when add new hospital
function myClear(){
  window.localStorage.clear();
}