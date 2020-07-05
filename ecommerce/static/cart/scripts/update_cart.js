function sendFormData(btn, productIdValue){
    console.log(btn.value)
    let frm = btn.parentElement;
    let action = document.createElement("input");
    let productId = document.createElement("input");
    action.setAttribute("type", "hidden")
    productId.setAttribute("type", "hidden")
    action.setAttribute("name", "action")
    productId.setAttribute("name", "product_id")
    action.setAttribute("value", btn.value)
    productId.setAttribute("value", productIdValue)
    frm.appendChild(action)
    frm.appendChild(productId)
    frm.submit()
}