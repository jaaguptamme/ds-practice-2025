describe('Page loads', () => {
  it('should load and show checkout message', () => {
    cy.visit('http://localhost:8080');
    cy.contains('Checkout Page');
  });
});

describe('Valid signular order', () => {
  it('should checkout and have the book counts updated', () => {
    cy.visit('http://localhost:8080');
    cy.contains('Submit Order').click();
    cy.contains('Order status: Order Approved',  { timeout: 10000 }).should('be.visible');
  });
});

describe('API test', () => {
  it('handles single order via API', async () => {
    let body = null;
   await cy.fixture('basic_order.json').then((data)=>{
            body=data;
        })
  const order1 =    { method: 'POST',
        url: 'http://localhost:8081/checkout',
        body: body
    };
  cy.wrap(Promise.all([
    cy.request(order1),
  ])).then((responses) => {
    responses.forEach(response => {
      expect(response.status).to.eq(200);
      cy.log(response);
    });
  });
}); 
}
)