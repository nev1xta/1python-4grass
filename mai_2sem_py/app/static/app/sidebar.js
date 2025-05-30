document.addEventListener('DOMContentLoaded', function() {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.querySelector('.toggle-btn');
  const overlay = document.querySelector('.sidebar-overlay');
  const sidebarItems = document.querySelectorAll('.sidebar-item');
  
  // Toggle sidebar
  function toggleSidebar() {
    sidebar.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
  }
  
  // Handle item clicks
  function handleItemClick(event) {
    // Remove active class from all items
    sidebarItems.forEach(item => {
      item.classList.remove('active');
    });
    
    // Add active class to clicked item
    const clickedItem = event.currentTarget;
    clickedItem.classList.add('active');
    
    // Store active item in localStorage (THIS IS WHERE IT GOES)
    const itemText = clickedItem.querySelector('span').textContent;
    localStorage.setItem('lastActiveItem', itemText);
  }
  
  // Initialize
  function initSidebar() {
    // Set click handlers for all items
    sidebarItems.forEach(item => {
      item.addEventListener('click', handleItemClick);
    });
    
    // Restore last active item from localStorage
    const lastActiveText = localStorage.getItem('lastActiveItem');
    if (lastActiveText) {
      sidebarItems.forEach(item => {
        if (item.querySelector('span').textContent === lastActiveText) {
          item.classList.add('active');
        }
      });
    }
    
    // Restore collapsed state
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
      sidebar.classList.add('collapsed');
    }
  }
  
  // Mobile toggle
  function toggleMobileSidebar() {
    sidebar.classList.toggle('open');
  }
  
  // Event listeners
  toggleBtn.addEventListener('click', function() {
    if (window.innerWidth <= 768) {
      toggleMobileSidebar();
    } else {
      toggleSidebar();
    }
  });
  
  if (overlay) {
    overlay.addEventListener('click', toggleMobileSidebar);
  }
  
  // Initialize everything
  initSidebar();
});