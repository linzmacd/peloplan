
document.querySelector('a.nav-link.page-profile').classList.add('active');

const unFollowButtons = document.querySelectorAll('.unfollow-user');
for (const unFollowButton of unFollowButtons) {
  unFollowButton.addEventListener('click', (event) => {
    event.preventDefault();
    const friendId = unFollowButton.value;
    fetch(`/unfollow/${friendId}`)
    .then((response) => response.json())
    .then((success) => {
      if (success) {
      location.reload();
      }
    });
  });
}

const fullSyncButton = document.querySelector('#full-peloton-sync')
fullSyncButton.addEventListener('click', (event) => {
  event.preventDefault();
  let syncModal = new bootstrap.Modal(document.getElementById('sync-modal'));
  syncModal.show();
  fetch('/full-peloton-sync')
  .then((response) => response.json())
  .then((success) => {
    if (success) {
      syncModal.hide();
      document.querySelector('#full-sync-blurb').innerHTML = `
      <p>Congratulations!</p>
      <p>You are fully synced!</p>
      `
    }
  });
});

// Update Profile Modal
const updateButton = document.querySelector('#update-profile');
updateButton.addEventListener('click', (event) => {
  event.preventDefault();
  let updateModal = new bootstrap.Modal(document.getElementById('update-modal'));
  updateModal.show();
});

// Find Friends Modal
const findFriendsButton = document.querySelector('#find-friends');
findFriendsButton.addEventListener('click', (event) => {
  event.preventDefault();
  let findFriendsModal = new bootstrap.Modal(document.getElementById('find-friends-modal'));
  findFriendsModal.show();
});

const findNameButton = document.querySelector('#search-names')
findNameButton.addEventListener('click', (event) => {
  const firstName = document.querySelector('#find-friend-fname').value;
  const lastName = document.querySelector('#find-friend-lname').value;
  fetch(`/find-by-name/${firstName}/${lastName}`)
  .then((response) => response.json())
  .then((friends) => {
    const results = document.querySelector('#find-friend-results')
    for (const friend of friends) {
      results.insertAdjacentHTML('beforeend', `
        <div class='row content-box modal-friend'>
          <div class='col-4'>
            ${friend.name}
          </div>
          <div class='col-4'>
            ${friend.email}
          </div>
          <div class='col-4'>
            <button class='follow-friend rb' value='${friend.user_id}'>Follow</button>
          </div>
        </div>
      `);
      const followFriendButtons = document.querySelectorAll('.follow-friend');
      for (const followFriendButton of followFriendButtons) {
        followFriendButton.addEventListener('click', (event) => {
          const friendId = followFriendButton.value;
          fetch(`/follow/${friendId}`)
          .then((response) => response.json())
          .then((success) => {
            if (success) {
              location.reload();
            }
          });
        });
      }
    }
  });
});

const findEmailButton = document.querySelector('#search-email')
findEmailButton.addEventListener('click', (event) => {
  const email = document.querySelector('#find-friend-email').value;
  fetch(`/find-by-email/${email}`)
  .then((response) => response.json())
  .then((friend) => {
    const results = document.querySelector('#find-friend-results');
    results.insertAdjacentHTML('beforeend', `
      <div class='row content-box modal-friend'>
        <div class='col-4'>
          ${friend.name}
        </div>
        <div class='col-4'>
          ${friend.email}
        </div>
        <div class='col-4'>
          <button class='follow-friend rb' value='${friend.user_id}'>Follow</button>
        </div>
      </div>
    `);
    const followFriendButtons = document.querySelectorAll('.follow-friend');
    for (const followFriendButton of followFriendButtons) {
      followFriendButton.addEventListener('click', (event) => {
        const friendId = followFriendButton.value;
        fetch(`/follow/${friendId}`)
        .then((response) => response.json())
        .then((success) => {
          if (success) {
            location.reload();
          }
        });
      });
    }
  });
});



// Invite Friends Modal
// const inviteFriendsButton = document.querySelector('#invite-friends');
// inviteFriendsButton.addEventListener('click', (event) => {
//   event.preventDefault();
//   let inviteFriendsModal = new bootstrap.Modal(document.getElementById('invite-friends-modal'));
//   inviteFriendsModal.show();
// });
