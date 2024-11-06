/*const navLinks = document.querySelectorAll('nav a');
const contentSections = document.querySelectorAll('main section');
const projectForm = document.getElementById('project-form');
const projectTable = document.getElementById('project-data');
  
  navLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const clickedSectionId = event.target.getAttribute('href').slice(1);
  
      contentSections.forEach(section => section.style.display = 'none');
      document.getElementById(clickedSectionId).style.display = 'block';
  
      document.getElementById(clickedSectionId).scrollIntoView({ behavior: 'smooth' });
  
      if (clickedSectionId === 'manage-projects') {
        projectTable.focus();
      }
    });
  });

    
  
  projectForm.addEventListener('submit', function(event) {
    event.preventDefault();
  
    const projectName = document.getElementById('project-name').value;
    const projectDescription = document.getElementById('project-description').value;
    const investmentGoal = document.getElementById('investment-goal').value;
    const location = document.getElementById('location').value;

    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    console.log('CSRF Token:', csrfToken);

    const formData = new FormData(); // Use FormData for form data
    formData.append('project_name', projectName);
    formData.append('description', projectDescription);
    formData.append('investment_goal', investmentGoal);
    formData.append('location', location);
    //formData.append('csrf_token', csrfToken); 
  
    // Send a POST request to Flask route to save project
    fetch('/create_project', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken, // Include CSRF token in headers
        //'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData, // Use formData instead of JSON.stringify
    })
    .then(response => {
      if (response.ok) {
        // If successful, add project to table
        addProjectToTable(formData);
        projectTable.dispatchEvent(new Event('scroll'));
        projectForm.reset();
        
        const manageProjectsLink = document.querySelector('nav a[href="#manage-projects"]');
        manageProjectsLink.click();
      } else {
        console.error('Failed to save project');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  
    function addProjectToTable(formData) {
      const tableRow = document.createElement('tr');
      const nameCell = document.createElement('td');
      const descriptionCell = document.createElement('td');
      const goalCell = document.createElement('td');
      const locationCell = document.createElement('td');
  
      nameCell.textContent = formData.get('project_name');
      descriptionCell.textContent = formData.get('description');
      goalCell.textContent = formData.get('investment_goal');
      locationCell.textContent = formData.get('location');
  
      tableRow.appendChild(nameCell);
      tableRow.appendChild(descriptionCell);
      tableRow.appendChild(goalCell);
      tableRow.appendChild(locationCell);
  
      projectTable.appendChild(tableRow);
    }  

    function displayManagedProjects() {
      fetch('/user_projects')
          .then(response => response.json())
          .then(data => {
              const projectsDiv = document.getElementById('manage-projects');
              projectsDiv.innerHTML = '';
              data.forEach(project => {
                  const projectElement = document.createElement('div');
                  projectElement.textContent = project.project_name;
                  projectsDiv.appendChild(projectElement);
              });
          })
          .catch(error => console.error('Error fetching projects:', error));
  }
  
  function displayProjectDetails(projectId) {
      fetch('/project_details/' + projectId)
          .then(response => response.json())
          .then(project => {
              const projectDetailsDiv = document.getElementById('data-visualization');
              projectDetailsDiv.innerHTML = '';
              const projectDetails = document.createElement('div');
              projectDetails.innerHTML = `
                  <p>Project Name: ${project.project_name}</p>
                  <p>Description: ${project.description}</p>
                  <p>Investment Goal: ${project.investment_goal}</p>
                  <p>Location: ${project.location}</p>
                  <p>Current Investment: ${project.current_investment}</p>
                  <p>ROI: ${project.roi}</p>
              `;
              projectDetailsDiv.appendChild(projectDetails);
          })
          .catch(error => console.error('Error fetching project details:', error));
  }
  
  // Example usage:
  displayManagedProjects(); // Display managed projects on page load
  
  // Example usage to display project details on click (assuming project IDs are available)
  // Replace projectId with the actual project ID
  const projectId = 1;
  displayProjectDetails(projectId);
  
});**/

const navLinks = document.querySelectorAll('nav a');
const contentSections = document.querySelectorAll('main section');
const projectForm = document.getElementById('project-form');
const projectTable = document.getElementById('project-data');

navLinks.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    const clickedSectionId = event.target.getAttribute('href').slice(1);

    contentSections.forEach(section => section.style.display = 'none');
    document.getElementById(clickedSectionId).style.display = 'block';

    document.getElementById(clickedSectionId).scrollIntoView({ behavior: 'smooth' });

    if (clickedSectionId === 'manage-projects') {
      projectTable.focus();
    }
  });
});

projectForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const projectName = document.getElementById('project-name').value;
  const projectDescription = document.getElementById('project-description').value;
  const investmentGoal = document.getElementById('investment-goal').value;
  const location = document.getElementById('location').value;

  const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  console.log('CSRF Token:', csrfToken);

  const formData = new FormData();
  formData.append('project_name', projectName);
  formData.append('description', projectDescription);
  formData.append('investment_goal', investmentGoal);
  formData.append('location', location);

  fetch('/create_project', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    body: formData,
  })
  .then(response => {
    if (response.ok) {
      addProjectToTable(formData);
      projectTable.dispatchEvent(new Event('scroll'));
      projectForm.reset();
      
      const manageProjectsLink = document.querySelector('nav a[href="#manage-projects"]');
      manageProjectsLink.click();
    } else {
      console.error('Failed to save project');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

function addProjectToTable(formData) {
  const tableRow = document.createElement('tr');
  const nameCell = document.createElement('td');
  const descriptionCell = document.createElement('td');
  const goalCell = document.createElement('td');
  const locationCell = document.createElement('td');

  nameCell.textContent = formData.get('project_name');
  descriptionCell.textContent = formData.get('description');
  goalCell.textContent = formData.get('investment_goal');
  locationCell.textContent = formData.get('location');

  tableRow.appendChild(nameCell);
  tableRow.appendChild(descriptionCell);
  tableRow.appendChild(goalCell);
  tableRow.appendChild(locationCell);

  projectTable.appendChild(tableRow);
}  

function displayManagedProjects(username) {
  fetch('/user_projects/' + username)
      .then(response => response.json())
      .then(data => {
          const projectsTableBody = document.getElementById('project-data');
          projectsTableBody.innerHTML = ''; // Clear existing data

          data.forEach(project => {
              const row = document.createElement('tr');

              const projectNameCell = document.createElement('td');
              projectNameCell.textContent = project.project_name;
              row.appendChild(projectNameCell);

              const descriptionCell = document.createElement('td');
              descriptionCell.textContent = project.description;
              row.appendChild(descriptionCell);

              const investmentGoalCell = document.createElement('td');
              investmentGoalCell.textContent = project.investment_goal;
              row.appendChild(investmentGoalCell);

              const locationCell = document.createElement('td');
              locationCell.textContent = project.location;
              row.appendChild(locationCell);

              projectsTableBody.appendChild(row);
          });
      })
      .catch(error => console.error('Error fetching projects:', error));
}

function displayProjectDetails(projectId) {
  fetch('/project_details/' + projectId)
      .then(response => response.json())
      .then(project => {
          const projectDetailsDiv = document.getElementById('data-visualization');
          projectDetailsDiv.innerHTML = '';
          const projectDetails = document.createElement('div');
          projectDetails.innerHTML = `
              <p>Project Name: ${project.project_name}</p>
              <p>Description: ${project.description}</p>
              <p>Investment Goal: ${project.investment_goal}</p>
              <p>Location: ${project.location}</p>
              <p>Current Investment: ${project.current_investment}</p>
              <p>ROI: ${project.roi}</p>
          `;
          projectDetailsDiv.appendChild(projectDetails);
      })
      .catch(error => console.error('Error fetching project details:', error));
}

// Example usage:
// Retrieve the username from the query parameters or any other source
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');

// Call the function with the actual username
displayManagedProjects(username);
// Display managed projects on page load

// Example usage to display project details on click (assuming project IDs are available)
// Replace projectId with the actual project ID
projectElement.addEventListener('click', function(event) {
  const projectId = event.target.dataset.projectId; // Assuming project ID is stored in a data attribute
  displayProjectDetails(projectId);
});


