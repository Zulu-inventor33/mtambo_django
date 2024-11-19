document.addEventListener("DOMContentLoaded", function () {

    // Sidebar navigation interaction
    const links = document.querySelectorAll('.sidebar ul li a');
    const sections = document.querySelectorAll('section');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const target = link.getAttribute('href').substring(1);
            sections.forEach(section => {
                section.classList.add('hidden');
                if (section.id === target) {
                    section.classList.remove('hidden');
                }
            });
        });
    });

    // Dummy data for all sections
    const todaysJobs = [
        { jobId: "NGA-LIFT1-10/11-01", building: "Ngara Flats", liftId: "Lift1", status: "Completed" },
        { jobId: "NGF-LIFT2-10/11-02", building: "Ngara Flats", liftId: "Lift2", status: "Pending" },
        { jobId: "GMM-LIFT1-10/11-01", building: "Green Mews", liftId: "Lift1", status: "Overdue" }
    ];

    const technicianActivity = [
        { name: "Mark Mwenda", assigned: 5, completed: 3, pending: 2 },
        { name: "Lucy Wambui", assigned: 4, completed: 4, pending: 0 },
        { name: "John Njoroge", assigned: 6, completed: 2, pending: 4 }
    ];

    const buildings = [
        { name: "Ngara Flats", lifts: "Lift1, Lift2", address: "Ngara, Nairobi", contact: "123-456-789" },
        { name: "Green Mews", lifts: "Lift1", address: "Westlands, Nairobi", contact: "987-654-321" }
    ];

    const technicians = [
        { name: "Mark Mwenda", contact: "123-456-789", dateJoined: "2022-01-01", completed: 30, pending: 5, overdue: 2 },
        { name: "Lucy Wambui", contact: "987-654-321", dateJoined: "2021-03-12", completed: 40, pending: 0, overdue: 0 }
    ];

    const claims = [
        { building: "Ngara Flats", jobId: "NGA-LIFT1-10/11-01", technician: "Mark Mwenda", liftId: "Lift1", jobDescription: "Noise from motor", claimStatus: "Filed" },
        { building: "Green Mews", jobId: "GMM-LIFT1-10/11-01", technician: "Lucy Wambui", liftId: "Lift1", jobDescription: "Not operational", claimStatus: "Filed" }
    ];

    const loggedIssues = [
        { developer: "Myspace Developers", date: "2024-10-10", building: "Ngara Flats", liftId: "Lift1", issue: "Motor failure" },
        { developer: "Techspace Ltd.", date: "2024-11-05", building: "Green Mews", liftId: "Lift1", issue: "Overheating" }
    ];

    const alerts = [
        { type: "New Technician Registration", message: "Mark Mwenda wants to register", date: "2024-11-19" },
        { type: "Issue Logged", message: "Myspace Developers logged an issue on Lift1", date: "2024-10-11" }
    ];

    // Fill Today's Jobs Table
    const todaysJobsTable = document.querySelector('#todays-jobs');
    todaysJobs.forEach(job => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${job.jobId}</td><td>${job.building}</td><td>${job.liftId}</td><td>${job.status}</td><td><button>View Task</button></td>`;
        todaysJobsTable.appendChild(row);
    });

    // Fill Technician Activity Tracker
    const technicianActivityTable = document.querySelector('#technician-activity');
    technicianActivity.forEach(tech => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${tech.name}</td><td>${tech.assigned}</td><td>${tech.completed}</td><td>${tech.pending}</td><td><button>View Details</button></td>`;
        technicianActivityTable.appendChild(row);
    });

    // Fill Buildings List
    const buildingsList = document.querySelector('#buildings-list');
    buildings.forEach(building => {
        const row = document.createElement('tr');
        row.innerHTML = `<td><a href="#">${building.name}</a></td><td>${building.lifts}</td><td>${building.address}</td><td>${building.contact}</td><td><button>View Details</button></td>`;
        buildingsList.appendChild(row);
    });

    // Fill Technicians List
    const techniciansList = document.querySelector('#technicians-list');
    technicians.forEach(tech => {
        const row = document.createElement('tr');
        row.innerHTML = `<td><a href="#">${tech.name}</a></td><td>${tech.contact}</td><td>${tech.dateJoined}</td><td>${tech.completed}</td><td>${tech.pending}</td><td><button>View Details</button></td>`;
        techniciansList.appendChild(row);
    });

    // Fill Claims Table
    const claimsList = document.querySelector('#claims-list');
    claims.forEach(claim => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${claim.building}</td><td>${claim.jobId}</td><td>${claim.technician}</td><td>${claim.liftId}</td><td>${claim.jobDescription}</td><td>${claim.claimStatus}</td>`;
        claimsList.appendChild(row);
    });

    // Fill Logged Issues Table
    const issuesList = document.querySelector('#issues-list');
    loggedIssues.forEach(issue => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${issue.developer}</td><td>${issue.date}</td><td>${issue.building}</td><td>${issue.liftId}</td><td>${issue.issue}</td>`;
        issuesList.appendChild(row);
    });

    // Fill Alerts Table
    const alertsList = document.querySelector('#alerts-list');
    alerts.forEach(alert => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${alert.type}</td><td>${alert.message}</td><td>${alert.date}</td>`;
        alertsList.appendChild(row);
    });

});





