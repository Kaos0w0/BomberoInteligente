// En este archivo se definen las funciones para la carga de archivos mediante drag and drop y 
// mediante el selector de archivos del sistema. .

// Se define la función que se ejecuta cuando se suelta un archivo en el área especificada
function dropHandler(ev) {
  // Previene el comportamiento por defecto de los navegadores (Prevent que el archivo se abra)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Se usa la interfaz para acceder al archivo
    [...ev.dataTransfer.items].forEach((item, i) => {
      // Si no son archivos, se rechazan
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (file.name.split('.').pop() != "txt") {
          alert("El archivo debe ser de tipo txt");
          return;
        } else {
          reader = new FileReader();
          reader.onload = function(event) {
            let matrix_txt = matrix_creator(event.target.result);
            let displayArea = document.getElementById("fileDisplayArea");
            displayArea.value = matrix_txt;
            displayArea.dispatchEvent(new Event("input"));
          }
          reader.readAsText(file);
        }
      }
    });
  }
}

// Se define la función que se ejecuta cuando se arrastra un archivo
function dragOverHandler(ev) {
  // Previene el comportamiento por defecto de los navegadores (Prevent que el archivo se abra)
  ev.preventDefault();
}

function matrix_creator(text){
  text = text.replace(/(\r\n|\n|\r)/gm, "\n");
  let matrix = text.split("\n");
  let matrix_txt = "";
  for (let i = 0; i < matrix.length; i++) {  
      if(matrix[i] != ""){
          matrix[i] = matrix[i].split(" ");
          matrix_txt += matrix[i].toString() + "/";
      } else {
          matrix.splice(i, 1);
          i--;
      }
  }
  matrix_txt = matrix_txt.slice(0, -1);
  return matrix_txt;
}

document.addEventListener("DOMContentLoaded", function () {
  var pantallaCarga = document.querySelector(".pantalla-carga");
  var contenido = document.getElementById("container");

  var duracionCarga = 9000;

  setTimeout(function () {
      pantallaCarga.style.display = "none";
      contenido.style.display = "block";
  }, duracionCarga);
});