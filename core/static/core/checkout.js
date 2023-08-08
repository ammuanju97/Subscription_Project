var stripe = Stripe('pk_test_51MiYppSGNFKxiTC6JlCPgGtk2VFv6jHlpFZP3nhStwoiuEl2ymyKgK7tT5GO9UjTOc89vE3OgN9PvLUBtiZiySHE00ZHIhIp28');

var checkoutButton = document.getElementById('checkout-button');

checkoutButton.addEventListener('click', function() {
  stripe.redirectToCheckout({
    // Make the id field from the Checkout Session creation API response
    // available to this file, so you can provide it as argument here
    // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
    sessionId: sessionid
  }).then(function (result) {
    // If `redirectToCheckout` fails due to a browser or network
    // error, display the localized error message to your customer
    // using `result.error.message`.
  });
});