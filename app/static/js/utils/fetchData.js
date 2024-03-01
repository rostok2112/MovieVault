async function fetchData(url) {
    let data = null
    const loader = document.querySelector('.loader-overlay') 
    try {
      if(loader) {
        loader.style.display = 'flex';
      }
      
      const response = await fetch(url);
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      data = await response.text();
      alert(data);
    } catch (error) {
      alert('Error: ' + error);
    }

    if(loader) {
      loader.style.display = 'none';
    }

    location.reload(true);
  }