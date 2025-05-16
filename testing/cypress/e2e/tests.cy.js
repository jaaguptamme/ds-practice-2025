describe('Homepage', () => {
  it('should load and show welcome message', () => {
    cy.visit('http://localhost:8000'); // Change to your app's URL
    cy.contains('Welcome'); // Adjust to something real from your UI
  });
});