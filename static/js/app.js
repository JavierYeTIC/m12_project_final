document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/products');
    const products = await response.json();

    const productList = document.getElementById('product-list');
    products.forEach(product => {
        const productItem = document.createElement('div');
        productItem.classList.add('product-item');
        productItem.innerHTML = `
            <div><img src="${product.img}" alt="${product.name}"></div>
            <div class="product-info">
                <h2>${product.name}</h2>
                <p>${product.description}</p>
                <p>Precio: $${product.price}</p>
                <p>Stock: ${product.units}</p>
            </div>
        `;
        productList.appendChild(productItem);
        console.log(product.img);
    });
});
