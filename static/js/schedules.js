
// Schedule Buttons
// const previewButtons = document.querySelectorAll('.sched-preview')
// for (const previewButton of previewButtons) {
//   previewButton.addEventListener('click', () => {
//     const storageId = previewButton.value;
//     const url = `/preview-schedule/${storageId}`;
//     window.open(url)
//   })
// }

// const loadButtons = document.querySelectorAll('.sched-load')
// for (const loadButton of loadButtons) {
//   loadButton.addEventListener('click', () => {
//     const storageId = loadButton.value;
//     const title = document.querySelector(`#name-${storageId}`).innerText;
//     document.querySelector('#load-modal-title').dataset.id = storageId;
//     document.querySelector('#load-modal-title').innerText = title;
//     let loadModal = new bootstrap.Modal(document.getElementById('load-modal'));
//     loadModal.show();
//   })
// }

// const deleteButtons = document.querySelectorAll('.sched-delete')
// for (const deleteButton of deleteButtons) {
//   deleteButton.addEventListener('click', () => {
//     const storageId = deleteButton.value;
//     const title = document.querySelector(`#name-${storageId}`).innerText
//     document.querySelector('#delete-modal-title').dataset.id = storageId;
//     document.querySelector('#delete-modal-title').innerText = title;
//     let deleteModal = new bootstrap.Modal(document.getElementById('delete-modal'));
//     deleteModal.show();
//   })
// }

// Load Schedule Modal
document.querySelector('#load-schedule').addEventListener('click', (event) => {
  event.preventDefault();
  const formInputs = {
    storageId: document.querySelector('#modal-storage-id').value,
    startDate: document.querySelector('#load-start-date').value,
  }
  fetch('/load-schedule', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((response) => {
    window.location.href = '/peloplan'
  });
});


// Delete Schedule Modal
document.querySelector('#delete-schedule').addEventListener('click', (event) => {
  event.preventDefault();
  const formInputs = {
    storageId: document.querySelector('#delete-modal-title').dataset.id,
  }
  console.log(formInputs)
  fetch('/delete-schedule', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((response) => {
    location.reload();
  })
});