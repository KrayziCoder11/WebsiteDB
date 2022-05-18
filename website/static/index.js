function deleteComputer(serial) {
  fetch("/delete-computer", {
    method: "POST",
    body: JSON.stringify({ serial: serial }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
