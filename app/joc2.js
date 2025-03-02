const paraulaInput = document.getElementById("paraulaSecreta");
const togglePassword = document.getElementById("togglePassword");
const startButton = document.getElementById("startGame");
const paraulaMostrada = document.getElementById("paraulaMostrada");
const intentsRestantsElement = document.getElementById("intentsRestants");
const botonsLletres = document.getElementById("botonsLletres");
const imatgePenjat = document.getElementById("imatgePenjat");

let paraulaSecreta = [];
let paraulaUsuari = [];
let intentsRestants = 10;
let imatgeIndex = 0;

// Mostrar/Ocultar la paraula secreta
togglePassword.addEventListener("click", () => {
    paraulaInput.type = paraulaInput.type === "password" ? "text" : "password";
});

// Començar partida
startButton.addEventListener("click", () => {
    const paraula = paraulaInput.value.trim();
    if (paraula.length < 4 || /\d/.test(paraula)) {
        alert("La paraula ha de tenir almenys 4 caràcters i no pot contenir números.");
        return;
    }

    paraulaSecreta = paraula.toUpperCase().split("");
    paraulaUsuari = Array(paraulaSecreta.length).fill("_");
    paraulaMostrada.textContent = paraulaUsuari.join(" ");
    intentsRestants = 10;
    intentsRestantsElement.textContent = `Intents restants: ${intentsRestants}`;
    startButton.disabled = true;
    paraulaInput.disabled = true;
    generarBotons();
    actualitzarImatge();
});

// Generar botons de lletres
function generarBotons() {
    botonsLletres.innerHTML = "";
    for (let i = 65; i <= 90; i++) {
        const lletra = String.fromCharCode(i);
        const boto = document.createElement("button");
        boto.textContent = lletra;
        boto.addEventListener("click", () => manejarLletra(lletra, boto));
        botonsLletres.appendChild(boto);
    }
}

// Manejar la selecció de lletres
function manejarLletra(lletra, boto) {
    boto.disabled = true;

    if (paraulaSecreta.includes(lletra)) {
        paraulaSecreta.forEach((char, index) => {
            if (char === lletra) paraulaUsuari[index] = lletra;
        });
    } else {
        intentsRestants--;
        imatgeIndex++;
    }

    paraulaMostrada.textContent = paraulaUsuari.join(" ");
    intentsRestantsElement.textContent = `Intents restants: ${intentsRestants}`;
    actualitzarImatge();

    if (!paraulaUsuari.includes("_")) {
        alert("Has guanyat!");
        reiniciarPartida();
    } else if (intentsRestants === 0) {
        alert(`Has perdut! La paraula era ${paraulaSecreta.join("")}.`);
        reiniciarPartida();
    }
}

// Actualitzar imatge
function actualitzarImatge() {
    const imgIndexRevers = 9 - imatgeIndex; // Càlcul de l'índex invers
    imatgePenjat.src = `imatges_p2/img_${imgIndexRevers}.jpg`;
}

// Reiniciar partida
function reiniciarPartida() {
    startButton.disabled = false;
    paraulaInput.disabled = false;
    paraulaInput.value = "";
    botonsLletres.innerHTML = "";
    paraulaMostrada.textContent = "";
    intentsRestants = 10;
    imatgeIndex = 0;
    actualitzarImatge();
}
