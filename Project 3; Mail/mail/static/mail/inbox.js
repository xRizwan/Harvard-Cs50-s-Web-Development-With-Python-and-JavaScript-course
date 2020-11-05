document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function show_email(id) {

  displayedEmail = document.querySelector('#email-view')

  // Show email view and hide other views
  displayedEmail.style.display = "block";
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // getting email info from the API
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(response => {
    console.log(response)
    
    // if email is archived or else
    if (response.archived){
      someHTML = '<button class="btn btn-outline-primary" id="unarchive">UnArchive</button>'
    } else {
      someHTML = '<button class="btn btn-outline-primary" id="archive">Archive</button>'
    }

    displayedEmail.innerHTML = `<div>
    <div class="alert alert-primary" id="message-container"></div>
    <div><b>From:</b> ${response.sender}</div>
    <div><b>To:</b> ${response.recipients}</div>
    <div><b>Subject:</b> ${response.subject}</div>
    <div class="mail-timestamp"><b>Timestamp:</b> ${response.timestamp}</div>
    <button class="btn btn-outline-primary" id="replybtn" >Reply</button>
    ${someHTML}
    <hr/>
    <div>${response.body}</div>
    </div>`

    if (response.archived){
      console.log('already archived');
      document.querySelector('#unarchive').addEventListener('click', () => unarchive_email(response.id));
    } else {
      document.querySelector('#archive').addEventListener('click', () => archive_email(response.id));
    }

    document.querySelector('#replybtn').addEventListener('click', () => reply_email(response));
  })

  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    })
  })
  
}

function send_email(e) {
  // compose-form
  e.preventDefault();

  // gettings input values
  let sender = document.querySelector('#compose-sender');
  let receivers = document.querySelector('#compose-recipients');
  let subject = document.querySelector('#compose-subject');
  let message = document.querySelector('#compose-body');

  console.log(sender.value, receivers.value, subject.value, message.value)


  // Making a post request using Fetch to '/emails'

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: receivers.value,
      subject: subject.value,
      body: message.value,
    })
  })
  .then(result => result.json())
  .then(result => {
    console.log(result)
    let messField = document.querySelector('#message')

    // display the result to the user

    if (result.error){
      // if something went wrong
      messField.style.display = 'block';
      messField.className = 'alert alert-warning';
      messField.innerText = result.error;
    } else {

      // if successfully sent
      messField.style.display = 'block';
      messField.className = 'alert alert-success';
      messField.innerText = result.message;
    }
  })

  // clearing the inputs
  receivers.value = ''
  subject.value = ''
  message.value = ''
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // hide the message field
  messField = document.querySelector('#message').style.display = 'none';
}

function load_mailbox(mailbox) {
  emails_view = document.querySelector('#emails-view')
  
  // Show the mailbox and hide other views
  emails_view.style.display = 'block';
  document.querySelector('#email-view').style.display = "none";
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  // getting emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(response => {
    console.log(response);
    response.forEach(mail => {
      let containerDiv = document.createElement('div');
      let senderDiv = document.createElement('div');
      let messageDiv = document.createElement('div');
      let dateDiv = document.createElement('div');

      containerDiv.className = "email btn-outline-dark";
      senderDiv.className = "email-title";
      messageDiv.className = "email-message";
      dateDiv.className = "email-date";

      senderDiv.innerText = mail.sender;
      dateDiv.innerText = mail.timestamp;
      messageDiv.innerText = mail.body;

      containerDiv.appendChild(senderDiv);
      containerDiv.appendChild(messageDiv);
      containerDiv.appendChild(dateDiv);
      containerDiv.addEventListener('click', () => show_email(mail.id))

      emails_view.appendChild(containerDiv);
    })
  })
}

function archive_email(id){
  console.log(id + " archived");
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true,
    })
  }).then(() => {
    let container = document.querySelector('#message-container');
    container.style.display = "block";
    container.textContent = "Archived!";
  })
}

function unarchive_email(id){
  console.log(id + " archived");
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false,
    })
  }).then(() => {
    let container = document.querySelector('#message-container');
    container.style.display = "block";
    container.textContent = "Un-Archived!";
  })
}

function reply_email(data){
  console.log(data);

  // hiding and showing appropriate views
  compose_email();

  // reference to input fields
  let receiverField = document.querySelector('#compose-recipients')
  let subjectField = document.querySelector('#compose-subject')
  let bodyField = document.querySelector('#compose-body') 

  let subject;

  if (data.subject.substring(0, 3) === 'Re:') {
    subject = data.subject;
  } else {
    subject = 'Re: ' + data.subject;
  }

  let body = `On ${data.timestamp} ${data.sender} wrote: ` + data.body;

  // settings field value
  receiverField.value = data.recipients;
  subjectField.value = subject;
  bodyField.value = body;
}
