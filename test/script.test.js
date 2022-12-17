test('Checking the initial state of the application - every input should be set to null string', () => {
    document.body.innerHTML = `
    <input
				type="text"
				id="startingAddress"
				name="startingAddress"
				autocomplete="shipping address-line1"
                placeholder="141 Echo Avenue, Oakland, CA 94611"
                size="50"
	/>
    <input
                type="text"
                id="endingAddress"
                name="endingAddress"
                autocomplete="billing address-line1"
                placeholder="1123 Oakland Avenue, Piedmont, CA 94611"
                size="50"
    />
    <input type="text" id="minmax" name="minmax" placeholder="min OR max"/>
    <input type="text" id="variance" name="variance" placeholder="0-2"/>
  `;
  require('../script.js');

  const startingAddress = document.getElementById('startingAddress');
  const endingAddress = document.getElementById('endingAddress');
  const minmax = document.getElementById('minmax');
  const variance = document.getElementById('variance');
  const expectation = ['', '', '', ''];
  const reality = [startingAddress.value, endingAddress.value, minmax.value, variance.value];

  expect(reality).toBe(expectation);
});