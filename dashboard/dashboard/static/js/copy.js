function copy_api_key() {
  /* Get the text field */
  var copyText = document.getElementById("inp-api-key");
  var notif = document.getElementById("copy-notif");
  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

   /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.value);

  /* Alert the copied text */
  notif.innerHTML = 'Copied!';

}
