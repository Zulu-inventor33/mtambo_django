/*=============================================================================================
                When we scroll we want the header to change background to white color so
                that we can maintain contrast.
==============================================================================================*/
document.addEventListener('DOMContentLoaded', function() {
    // When we scroll, the header background change to white from transparent
    const desktopLinks = document.querySelectorAll('.desktop-link');
    const nav_open_btn = document.getElementById('nav-open');
    const header_section = document.getElementById('header-section');
    const logo_name = document.getElementById('logo-name');

    // Function to apply styles based on scroll position
    function updateHeaderStyles() {
        if (window.scrollY > 50) {
            header_section.classList.add('scrolled');
            desktopLinks.forEach(link => {
                link.classList.remove('text-white');
                link.classList.add('text-gray-700');
            });
            logo_name.classList.remove('text-white');
            logo_name.classList.add('text-gray-700');
            nav_open_btn.classList.remove('text-white');
            nav_open_btn.classList.add('text-black');
        } else {
            header_section.classList.remove('scrolled');
            desktopLinks.forEach(link => {
                link.classList.remove('text-gray-700');
                link.classList.add('text-white');
            });
            logo_name.classList.remove('text-gray-700');
            logo_name.classList.add('text-white');
            nav_open_btn.classList.remove('text-black');
            nav_open_btn.classList.add('text-white');
        }
    }

    // Initialize styles based on the current scroll position
    updateHeaderStyles();

    // Add scroll event listener to handle scroll-based style changes
    window.addEventListener('scroll', updateHeaderStyles);
});

/*=============================================================================================
                            REVIEWS SECTION
==============================================================================================*/
document.addEventListener('DOMContentLoaded', function() {
    const nextReviewBtn = document.querySelector('.right-arrow');
    const prevReviewBtn = document.querySelector('.left-arrow');
    const smallScreenNextBtn = document.querySelector('.right-arrow-btn');
    const smallScreenPrevBtn = document.querySelector('.left-arrow-btn');

    const reviews = [
        {
            text: "M-Tambo CMMS has transformed how we manage our building assets. It provides a clear view of all maintenance activities, helping us schedule tasks efficiently and reduce downtime. It's a game-changer for building managers like us!",
            name: "James Anderson - Building Manager, Green Tower Estates",
            stars: "★★★★★",
            image: "https://risersafe.com/wp-content/uploads/2023/04/RScircle_AM.webp"
        },
        {
            text: "As a maintenance service provider, M-Tambo has enabled us to streamline our operations. We can now easily track all job assignments, manage our team more effectively, and ensure high-quality service delivery to our clients",
            name: "Sarah Johnson - Operations Manager, TechMaintain Services",
            stars: "★★★★☆",
            image: "https://risersafe.com/wp-content/uploads/2023/04/RScircle_AM.webp"
        },
        {
            text: "M-Tambo has made a huge difference in how I work. I receive alerts for upcoming maintenance tasks and can log my activities on the go, ensuring nothing is missed. It's made my job much easier and more efficient.",
            name: "Michael Brown - Senior Technician, ABC Maintenance Co.",
            stars: "★★★★★",
            image: "https://risersafe.com/wp-content/uploads/2023/04/RScircle_AM.webp"
        },
    ];
    
    let currentReviewIndex = 0;

    function updateReview() {
        const reviewText = document.querySelector('.review-text');
        const clientImage = document.querySelector('.client-info-image');
        const clientName = document.querySelector('.client-name');
        const clientStars = document.querySelector('.stars');
        const clientImages = document.querySelectorAll('.client-image');
    
        reviewText.textContent = reviews[currentReviewIndex].text;
        clientImage.src = reviews[currentReviewIndex].image;
        clientName.textContent = reviews[currentReviewIndex].name;
        clientStars.textContent = reviews[currentReviewIndex].stars;
    
        clientImages.forEach((img, index) => {
            img.classList.remove('active');
            if (index === currentReviewIndex) {
                img.classList.add('active');
            }
        });
    }   
    
    function nextReview() {
        currentReviewIndex = (currentReviewIndex + 1) % reviews.length;
        updateReview();
    }

    function prevReview() {
        currentReviewIndex = (currentReviewIndex - 1 + reviews.length) % reviews.length;
        updateReview();
    }
    // Initial load
    updateReview();

    nextReviewBtn.addEventListener('click', function() {
        nextReview();
    })

    prevReviewBtn.addEventListener('click', function() {
        prevReview();
    })

    smallScreenNextBtn.addEventListener('click', function() {
        nextReview();
    })

    smallScreenPrevBtn.addEventListener('click', function() {
        prevReview();
    })
})