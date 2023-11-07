let mapa_juego = [];
let posicion_inicial = [];

function dibujarMatriz(matriz) {
    const matrizContainer = document.getElementById('matriz-container');
    
    // Limpia cualquier contenido anterior del contenedor
    matrizContainer.innerHTML = '';
  
    matriz = matriz.split("/");
    matriz.forEach((fila, rowIndex) => {
        matriz[rowIndex] = fila.split(",");
    });
    mapa_juego = matriz;
    // Recorre la matriz y crea elementos div para cada celda
    matriz.forEach((fila, rowIndex) => {
      const filaDiv = document.createElement('div');
      filaDiv.classList.add('fila');
      matrizContainer.appendChild(filaDiv);
  
      fila.forEach((valor, colIndex) => {
        const celdaDiv = document.createElement('div');
        celdaDiv.classList.add('celda');
        celdaDiv.id = `celda-${rowIndex}-${colIndex}`;
        if(valor == 5){
            posicion_inicial = [colIndex, rowIndex];
        }
        celdaDiv.style.backgroundImage = 'url(' + obtenerImagenPorValor(valor) + ')';
        filaDiv.appendChild(celdaDiv);
      });
    });
  }
  
  // Función para obtener la URL de la imagen basada en el valor en la matriz
  function obtenerImagenPorValor(valor) {
    // Lógica para asignar una imagen a cada valor de la matriz
    switch(valor){
        case '0':
            image = "./static/images/ground.png";
            break;
        case '1':
            image = "./static/images/wall.png";
            break;
        case '2':
            image = "./static/images/fire.png";
            break;
        case '3':
            image = "./static/images/bucket1.png";
            break;
        case '4':
            image = "./static/images/bucket2.png";
            break;
        case '5':
            image = "./static/images/fireman_start.png";
            break;
        case '6':
            image  = "./static/images/hydrant.png";
            break;
    }
    return image;
  }

function dibujar_solucion(solucion){
    tiempo = Array.from(solucion)[1]
    nodos_expandidos = Array.from(solucion)[2]
    costo = Array.from(solucion)[3]
    profundidad = Array.from(solucion)[4]
    solucion = Array.from(Array.from(solucion)[0]);    
    const pasoActualElement = document.getElementById('paso-actual');
    const iniciarBusqueda = document.getElementById('algoritmos-container');
    iniciarBusqueda.style.display = 'none'; 

    let pasoActualIndex = 0;

    function mostrarSiguientePaso() {
        if (pasoActualIndex < solucion.length) {
        const pasoActual = solucion[pasoActualIndex];
        pasoActualElement.textContent = `Paso actual: ${pasoActual}`;

        actualizar_mapa(pasoActual)

        pasoActualIndex++;
        if (pasoActualIndex == solucion.length){
            mostrarResultado(tiempo, nodos_expandidos, costo, profundidad, 1);
        }
        // Espera un tiempo antes de mostrar el siguiente paso (puedes ajustar el tiempo)
        setTimeout(mostrarSiguientePaso, 500);
        }
    }
    mostrarSiguientePaso();
}

function actualizar_mapa(paso_actual){
    let direccion_accion = paso_actual.split(" y ");
    const cubeta1 = document.getElementById('cubeta1');
    const cubeta2 = document.getElementById('cubeta2');
    let x = posicion_inicial[0];
    let y = posicion_inicial[1];
    let cubeta = '0';
    let litros_cubeta = 0;
    let nuevo_x = x;
    let nuevo_y = y;
    switch(direccion_accion[0]){
        case 'arriba':
            nuevo_y = y - 1;
            break;
        case 'abajo':
            nuevo_y = y + 1;
            break;
        case 'izquierda':
            nuevo_x = x - 1;
            break;
        case 'derecha':
            nuevo_x = x + 1;
            break;
    }

    let celda_anterior = mapa_juego[y][x];
    let celda_nueva = mapa_juego[nuevo_y][nuevo_x];
    let celda_anterior_img = '';
    let celda_nueva_img = '';

    switch (celda_anterior) {
        case '5':
            celda_anterior_img = "./static/images/start.png";
            break;
        case '6':
            celda_anterior_img = "./static/images/hydrant.png";
            break;
        default:
            celda_anterior_img = "./static/images/ground.png";
            break;
    }

    switch (direccion_accion[1]) {
        case 'apagar_fuego':
            celda_nueva_img = "./static/images/fireman_ashes.png";
            let cubeta1_llena = (window.getComputedStyle(cubeta1).getPropertyValue("background-image")).match(/url\(([^)]+)\)/i);
            if(cubeta2.style.backgroundImage !== ''){
                let cubeta2_llena = (window.getComputedStyle(cubeta2).getPropertyValue("background-image")).match(/url\(([^)]+)\)/i);
                if(cubeta1_llena[0].includes('full_bucket') && cubeta2_llena[0].includes('full_bucket')){
                    cubeta2.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
                } else if (cubeta1_llena[0].includes('full_bucket') && !cubeta2_llena[0].includes('full_bucket')){
                    cubeta1.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
                }
            } else {
                cubeta1.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
            }
            
            break;
        case 'recoger_cubeta_pequena':
            celda_nueva_img = "./static/images/fireman.png";
            cubeta1.style.display = 'block';
            cubeta1.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
            break;
        case 'recoger_cubeta_grande':
            celda_nueva_img = "./static/images/fireman.png";
            cubeta1.style.display = 'block';
            cubeta2.style.display = 'block';
            cubeta1.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
            cubeta2.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
            break;
        case 'llenar_cubeta':
            celda_nueva_img = "./static/images/fireman_fill.png";
            if(window.getComputedStyle(cubeta2).display != 'block'){
                cubeta1.style.backgroundImage = 'url(./static/images/full_bucket.png)';
            } else if (window.getComputedStyle(cubeta2).display == 'block'){
                cubeta1.style.backgroundImage = 'url(./static/images/full_bucket.png)';
                cubeta2.style.backgroundImage = 'url(./static/images/full_bucket.png)';
            }
            break;

        case undefined:
            if(celda_nueva == '0'){
                celda_nueva_img = "./static/images/fireman.png";
            } else if (celda_nueva == '5'){
                celda_nueva_img = "./static/images/fireman_start.png";
            } else if (celda_nueva == '6'){
                celda_nueva_img = "./static/images/fireman_hydrant.png";
            } else {
                celda_nueva_img = "./static/images/fireman.png";
            }
            break;                
    }

    let div_celda_anterior = document.getElementById(`celda-${y}-${x}`);
    div_celda_anterior.style.backgroundImage = 'url(' + celda_anterior_img + ')';
    let div_celda_nueva = document.getElementById(`celda-${nuevo_y}-${nuevo_x}`);
    div_celda_nueva.style.backgroundImage = 'url(' + celda_nueva_img + ')';
    posicion_inicial = [nuevo_x, nuevo_y];
}

function mostrarResultado(tiempo, nodosExpandidos, costo, profundidad, hay_solucion) {
    var resultadoContainer = document.getElementById('resultado-container');
    resultadoContainer.style.display = 'block';
    const iniciarBusqueda = document.getElementById('algoritmos-container');
    iniciarBusqueda.style.display = 'none'; 
  
    if(hay_solucion == 1){
        var resultadoHTML = `
        <h2>Resultado:</h2>
        <p style="color: white;">Tiempo: ${tiempo} segundos</p>
        <p style="color: white;">Nodos Expandidos: ${nodosExpandidos}</p>
        <p style="color: white;">Costo: ${costo}</p>
        <p style="color: white;">Profundidad: ${profundidad}</p>
        <button onclick="volver()">Volver</button>
      `;
    } else {
        var resultadoHTML = `
        <h2>Resultado:</h2>
        <p style="color: white;">No hay solución</p>
        <button onclick="volver()">Volver</button>
      `;
    }
   
  
    resultadoContainer.innerHTML = resultadoHTML;
  
    resultadoContainer.style.display = 'flex';
    resultadoContainer.style.flexDirection = 'column';
    resultadoContainer.style.alignItems = 'center';
    resultadoContainer.style.justifyContent = 'center';

    body = document.body;
    body.appendChild(resultadoContainer);
  }
  
  function volver() {
    // Ocultar el contenedor de resultados y mostrar las opciones de búsqueda nuevamente
    var resultadoContainer = document.getElementById('resultado-container');
    if (resultadoContainer) {
      resultadoContainer.style.display = 'none';
    }
    var algoritmosContainer = document.getElementById('algoritmos-container');
    if (algoritmosContainer) {
      algoritmosContainer.style.display = 'block';
    }

    reiniciar_matrix();
  }

    function reiniciar_matrix(){
        const cubeta1 = document.getElementById('cubeta1');
        const cubeta2 = document.getElementById('cubeta2');
        cubeta1.style.display = 'none';
        cubeta2.style.display = 'none';
        cubeta1.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
        cubeta2.style.backgroundImage = 'url(./static/images/empty_bucket.png)';
        
        mapa_juego.forEach((fila, rowIndex) => {        
            fila.forEach((valor, colIndex) => {
                if(valor == 5){
                    posicion_inicial = [colIndex, rowIndex];
                }
              const celdaDiv = document.getElementById(`celda-${rowIndex}-${colIndex}`);
              celdaDiv.style.backgroundImage = 'url(' + obtenerImagenPorValor(valor) + ')';
            });
          });
    }
