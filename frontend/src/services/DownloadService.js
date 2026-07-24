export const downloadFile = (response, defaultFilename, mimeType) => {
  const blob = new Blob([response.data], {
    type: mimeType,
  });

  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;

  const disposition =
    response.headers["content-disposition"];

  let filename = defaultFilename;

  if (disposition) {
    const match = disposition.match(
      /filename="?([^"]+)"?/
    );

    if (match?.[1]) {
      filename = match[1];
    }
  }

  link.download = filename;

  document.body.appendChild(link);

  link.click();

  link.remove();

  window.URL.revokeObjectURL(url);
};