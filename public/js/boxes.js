document.addEventListener('DOMContentLoaded', async () => {
    const boxesContainer = document.getElementById('boxes-container');
    try {
      // 1) Fetch the JSON
      const response = await fetch('/api/boxes');
      if (!response.ok) throw new Error("Failed to fetch boxes data");
      
      const data = await response.json();
      if(!Array.isArray(data)) {
        throw new Error("boxes_data.json is not an array");
      }
  
      // 2) Randomly pick some items or show them all
      //    If you want a single random entry, do:
      // const randomItem = data[Math.floor(Math.random() * data.length)];
      // const boxesToRender = [randomItem];
      
      // Or if you want all in random order:
      const boxesToRender = shuffleArray(data); // We'll define shuffleArray below
  
      // 3) Create a box div for each item
      boxesToRender.forEach(item => {
        const boxDiv = document.createElement('div');
        boxDiv.className = 'text-box';
        boxDiv.textContent = item.text;  // The text from JSON
  
        // 4) On click, open the .md file in a new tab or show in a modal
        boxDiv.addEventListener('click', () => {
          // Option A: open in a new tab
          window.open(`/api/md/${encodeURIComponent(item.mdFile)}`, '_blank');
        });
  
        // Append to container
        boxesContainer.appendChild(boxDiv);
      });
  
    } catch (err) {
      console.error(err);
      boxesContainer.innerHTML = '<p>Error loading boxes data.</p>';
    }
  });
  
  // A helper function to shuffle an array in-place
  function shuffleArray(array) {
    for(let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
  