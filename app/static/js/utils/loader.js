function appendLoader() {
    const loader_overlay = document.createElement("div");
    loader_overlay.classList.add("loader-overlay");
  
    const loader = document.createElement("div");
    loader.classList.add("loader");
  
    loader_overlay.append(loader);
  
    document.body.append(loader_overlay)
  
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        .loader-overlay {
          display: none;
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(255, 255, 255, 0.8);
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        .loader {
          border: 16px solid #f3f3f3;
          border-top: 16px solid #3498db;
          border-radius: 50%;
          width: 80px;
          height: 80px;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `
    document.head.appendChild(styleSheet); 
  
    return true;
  }
  
  document.addEventListener('DOMContentLoaded', appendLoader);
