document.addEventListener("DOMContentLoaded", async () => {
  const section = document.querySelector("section");
  const paymentIntentUrl = section.getAttribute("data-payment-intent-url");
  const stripePublicKey = section.getAttribute("data-stripe-public-key");

  const stripe = Stripe(stripePublicKey);
  let elements;

  let clientSecret = "";
  try {
    const response = await fetch(paymentIntentUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({email: document.getElementById('email').value})
    });
    const data = await response.json();
    clientSecret = data.clientSecret;
  } catch (error) {
    console.error("Erro ao obter o clientSecret:", error);
    showMessage("Erro ao obter o clientSecret. Tente novamente.");
    return;
  }

  elements = stripe.elements({ clientSecret });

  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");

  const form = document.getElementById("payment-form");
  form.addEventListener("submit", async (event) => {
    setLoading(true);
    event.preventDefault();
    const email = document.getElementById('email').value;
  
    try {
      const result = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: "http://127.0.0.1:8000/produtos/",
          payment_method_data: {
            billing_details: {
              email: email
            }
          }
        },
      });
  
      setLoading(false);
  
      if (result.error) {
        showMessage("Ocorreu um erro: " + result.error.message);
      } else if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
        showMessage("Compra finalizada com sucesso!");
        paymentElement.clear()
      } else {
        showMessage("Pagamento em processamento. Por favor, aguarde.");
      }
    } catch (error) {
      setLoading(false);
      showMessage("Erro na comunicação com o servidor. Tente novamente.");
      console.error("Erro:", error);
    }
  });
  

  function showMessage(messageText) {
    const messageContainer = document.querySelector("#payment-message");

    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;

    setTimeout(function () {
      messageContainer.classList.add("hidden");
      messageContainer.textContent = "";
    }, 4000);
  }

  function setLoading(isLoading) {
    if (isLoading) {
      document.querySelector("#submit").disabled = true;
      document.querySelector("#spinner").classList.remove("hidden");
      document.querySelector("#button-text").classList.add("hidden");
    } else {
      document.querySelector("#submit").disabled = false;
      document.querySelector("#spinner").classList.add("hidden");
      document.querySelector("#button-text").classList.remove("hidden");
    }
  }
});
