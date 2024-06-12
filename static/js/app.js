document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/products');
    const products = await response.json();

    const productList = document.getElementById('product-list');
    products.forEach(product => {
        const productItem = document.createElement('div');
        productItem.innerHTML = `
            <h2>${product.name}</h2>
            <img src="${product.img}">
            <p>${product.description}</p>
            <p>Precio: $${product.price}</p>
            <p>Stock: ${product.units}</p>
        `;
        productList.appendChild(productItem);
        console.log(product.img)
    });
});
