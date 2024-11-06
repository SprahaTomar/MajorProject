const projects = [
    {
      name: "Project 1",
      description: "Description of Project 1",
      goal: 10000,
      investedAmount: 5000, // Amount invested in the project
      roi: 15, // Return on Investment percentage
      completed: true, // Project completion status (boolean)
    },
    {
      name: "Project 2",
      description: "Description of Project 2",
      goal: 20000,
      investedAmount: 8000, // Amount invested in the project
      roi: 10, // Return on Investment percentage
      completed: false, // Project completion status (boolean)
    },
    // ... Add more projects as needed
  ];
  
  // Function to create a table row for a project
  function createProjectTableRow(project) {
    const tableRow = document.createElement('tr');
    const nameCell = document.createElement('td');
    const descriptionCell = document.createElement('td');
    const goalCell = document.createElement('td');
    const investedAmountCell = document.createElement('td');
    const roiCell = document.createElement('td');
    const completedCell = document.createElement('td');
  
    nameCell.textContent = project.name;
    descriptionCell.textContent = project.description;
    goalCell.textContent = project.goal;
    investedAmountCell.textContent = project.investedAmount;
    //roiCell.textContent = ${project.roi}%; // Display ROI percentage
    completedCell.textContent = project.completed ? "Yes" : "No";
  
    tableRow.appendChild(nameCell);
    tableRow.appendChild(descriptionCell);
    tableRow.appendChild(goalCell);
    tableRow.appendChild(investedAmountCell);
    tableRow.appendChild(roiCell);
    tableRow.appendChild(completedCell);
  
    return tableRow;
  }
  
  // Populate the project table with initial data (replace with your actual data fetching)
  const projectTable = document.getElementById('project-data');
  projects.forEach(project => {
    const tableRow = createProjectTableRow(project);
    projectTable.appendChild(tableRow);
  });
  
  // Handle navigation link clicks (simplified for brevity)
  const navLinks = document.querySelectorAll('nav a');
  navLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const clickedSectionId = event.target.getAttribute('href').slice(1);
      const sections = document.querySelectorAll('main section');
      sections.forEach(section => section.style.display = 'none');
      document.getElementById(clickedSectionId).style.display = 'block';
    });
  });