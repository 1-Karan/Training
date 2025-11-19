////document.addEventListener("DOMContentLoaded", () => {
////  // Show selected file name
////  const fileInput = document.querySelector('input[type="file"]');
////  if (fileInput) {
////    fileInput.addEventListener("change", () => {
////      const label = document.createElement("p");
////      label.textContent = `Selected file: ${fileInput.files[0].name}`;
////      fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
////    });
////  }
////
////  // Collect selected recipients into a hidden input
////  const emailForm = document.getElementById("email-form");
////  if (emailForm) {
////    emailForm.addEventListener("submit", (e) => {
////      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
////      const selected = Array.from(checkboxes).map(cb => cb.value);
////      const hiddenInput = document.createElement("input");
////      hiddenInput.type = "hidden";
////      hiddenInput.name = "recipients";
////      hiddenInput.value = selected.join(",");
////      emailForm.appendChild(hiddenInput);
////    });
////  }
////});
////document.addEventListener("DOMContentLoaded", () => {
////  const analyzeForm = document.querySelector('form[action="/analyze_meeting/"]');
////  const loading = document.getElementById("loading-animation");
////
////  if (analyzeForm && loading) {
////    analyzeForm.addEventListener("submit", () => {
////      loading.style.display = "block";
////    });
////  }
////
////  // Optional: hide animation after page reload
////  window.addEventListener("pageshow", () => {
////    if (loading) loading.style.display = "none";
////  });
////});
////
////document.addEventListener("DOMContentLoaded", () => {
////  // Show loading animation on Analyze Transcript
////  const analyzeForm = document.getElementById("analyze-form");
////  const loading = document.getElementById("loading-animation");
////
////  if (analyzeForm && loading) {
////    analyzeForm.addEventListener("submit", () => {
////      loading.style.display = "block";
////    });
////  }
////
////  // Collect selected recipients into a hidden input
////  const emailForm = document.getElementById("email-form");
////  if (emailForm) {
////    emailForm.addEventListener("submit", (e) => {
////      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
////      const selected = Array.from(checkboxes).map(cb => cb.value);
////      const hiddenInput = document.createElement("input");
////      hiddenInput.type = "hidden";
////      hiddenInput.name = "recipients";
////      hiddenInput.value = selected.join(",");
////      emailForm.appendChild(hiddenInput);
////    });
////  }
////})
////
//
//
//document.addEventListener("DOMContentLoaded", () => {
//  // Show selected file name
//  const fileInput = document.querySelector('input[type="file"]');
//  if (fileInput) {
//    fileInput.addEventListener("change", () => {
//      const label = document.createElement("p");
//      label.textContent = `Selected file: ${fileInput.files[0].name}`;
//      fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
//    });
//  }
//
//  // Analyze Transcript loading
//  const analyzeForm = document.querySelector('form[action="/analyze_meeting/"]');
//  const loading = document.getElementById("loading-animation");
//  if (analyzeForm && loading) {
//    analyzeForm.addEventListener("submit", () => {
//      loading.style.display = "block";
//    });
//  }
//
//  // Email form handling
//  const emailForm = document.getElementById("email-form");
//  const emailLoading = document.getElementById("email-loading");
//  if (emailForm) {
//    emailForm.addEventListener("submit", (e) => {
//      // Collect selected recipients
//      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
//      const selected = Array.from(checkboxes).map(cb => cb.value);
//      const hiddenInput = document.createElement("input");
//      hiddenInput.type = "hidden";
//      hiddenInput.name = "recipients";
//      hiddenInput.value = selected.join(",");
//      emailForm.appendChild(hiddenInput);
//
//      // Show email loading animation
//      if (emailLoading) {
//        emailLoading.style.display = "block";
//      }
//
//      // Disable button to prevent double clicks
//      const btn = emailForm.querySelector("button[type='submit']");
//      if (btn) {
//        btn.disabled = true;
//        btn.textContent = "Processing...";
//      }
//    });
//  }
//});
//

document.addEventListener("DOMContentLoaded", () => {
  // Popup system
  const popup = document.getElementById("popup");
  const popupMessage = document.getElementById("popup-message");
  const popupClose = document.getElementById("popup-close");

  function showPopup(message) {
    popupMessage.textContent = message;
    popup.style.display = "flex";
  }

  popupClose.addEventListener("click", () => {
    popup.style.display = "none";
  });

  // Show selected file name
//  const fileInput = document.querySelector('input[type="file"]');
//  if (fileInput) {
//    fileInput.addEventListener("change", () => {
//      const label = document.createElement("p");
//      label.textContent = `Selected file: ${fileInput.files[0].name}`;
//      fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
//    });
//  }
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      // Remove any existing label first
      const oldLabel = fileInput.parentNode.querySelector(".file-label");
      if (oldLabel) oldLabel.remove();

      // Add new label
      const label = document.createElement("p");
      label.className = "file-label";
      label.textContent = `Selected file: ${fileInput.files[0].name}`;
      fileInput.parentNode.insertBefore(label, fileInput.nextSibling);
    });
  }
});


  // Analyze Transcript loading (Magnifier)
  const analyzeForm = document.querySelector('form[action="/analyze_meeting/"]');
  const analyzeLoading = document.getElementById("analyze-loading");
  if (analyzeForm && analyzeLoading) {
    analyzeForm.addEventListener("submit", () => {
      analyzeLoading.style.display = "block";
    });
  }

  // Email form handling (Spinner)
  const emailForm = document.getElementById("email-form");
  const emailLoading = document.getElementById("email-loading");
  if (emailForm) {
    emailForm.addEventListener("submit", (e) => {
      // Collect selected recipients
      const checkboxes = emailForm.querySelectorAll('input[name="recipients"]:checked');
      const selected = Array.from(checkboxes).map(cb => cb.value);
      const hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "recipients";
      hiddenInput.value = selected.join(",");
      emailForm.appendChild(hiddenInput);

      // Show email loading animation
      if (emailLoading) emailLoading.style.display = "block";

      // Disable button
      const btn = emailForm.querySelector("button[type='submit']");
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Processing...";
      }
    });
  }

  // Reminders form handling (Spinner)
  const reminderForm = document.getElementById("reminder-form");
  const reminderLoading = document.getElementById("reminder-loading");
  if (reminderForm && reminderLoading) {
    reminderForm.addEventListener("submit", () => {
      reminderLoading.style.display = "block";
    });
  }

  // ✅ Show popup if server sends success message
  const successMessage = document.querySelector(".success");
  if (successMessage) {
    if (successMessage.textContent.includes("Email sent successfully")) {
      showPopup("✅ Email sent successfully!");
    } else if (successMessage.textContent.includes("Reminders successfully added")) {
      showPopup("✅ Reminders added to calendar!");
    }
  }
});

