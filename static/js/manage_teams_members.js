const teamTable = document.getElementById('team-table');
const quitForm = document.getElementById('quit-team');

const userTable = document.getElementById('user-table');
const addToTeamForm = document.getElementById('add-to-team');

let checkedTeams = [];
let checkedUsers = [];

// Update checked teams
function updateCheckedTeams() {
  checkedTeams = Array.from(teamTable.querySelectorAll('input[type="checkbox"]:checked'))
                      .map(cb => cb.value);

  // Show quit form if any team is checked
  quitForm.style.display = checkedTeams.length > 0 ? 'flex' : 'none';

  // Re-evaluate add-to-team form
  updateCheckedUsers();
}

// Update checked users
function updateCheckedUsers() {
  checkedUsers = Array.from(userTable.querySelectorAll('input[type="checkbox"]:checked'))
                      .map(cb => cb.value);

  // Show add-to-team form only if exactly one team AND ≥1 user selected
  addToTeamForm.style.display = (checkedTeams.length === 1 && checkedUsers.length > 0) ? 'flex' : 'none';
}

// Event listener for team checkboxes
teamTable.addEventListener('change', (e) => {
  if (e.target && e.target.type === 'checkbox') {
    updateCheckedTeams();
  }
});

// Event listener for user checkboxes
userTable.addEventListener('change', (e) => {
  if (e.target && e.target.type === 'checkbox') {
    updateCheckedUsers();
  }
});

// Add checked teams to quit form before submission
quitForm.addEventListener('submit', (e) => {
  // Remove previous hidden inputs
  quitForm.querySelectorAll('.hidden-team-input').forEach(el => el.remove());
  // Add current checked teams
  checkedTeams.forEach(team => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'select_team';
    input.value = team;
    input.classList.add('hidden-team-input');
    quitForm.appendChild(input);
  });
});

// Add selected team + users to add-to-team form before submission
addToTeamForm.addEventListener('submit', (e) => {
  // Remove previous hidden inputs
  addToTeamForm.querySelectorAll('.hidden-input').forEach(el => el.remove());

  // Add the selected team (exactly one)
  const teamInput = document.createElement('input');
  teamInput.type = 'hidden';
  teamInput.name = 'select_team';
  teamInput.value = checkedTeams[0]; // exactly one team
  teamInput.classList.add('hidden-input');
  addToTeamForm.appendChild(teamInput);

  // Add selected users
  checkedUsers.forEach(user => {
    const userInput = document.createElement('input');
    userInput.type = 'hidden';
    userInput.name = 'select_user';
    userInput.value = user;
    userInput.classList.add('hidden-input');
    addToTeamForm.appendChild(userInput);
  });

  if (checkedUsers.length === 0 || checkedTeams.length !== 1) {
    e.preventDefault();
    alert('Select exactly one team and at least one user.');
  }
});