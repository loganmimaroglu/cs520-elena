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
  //require('cs520-elena/src/script.js');

  const startingAddress = document.getElementById('startingAddress');
  const endingAddress = document.getElementById('endingAddress');
  const minmax = document.getElementById('minmax');
  const variance = document.getElementById('variance');

  expect(startingAddress.value).toBe('');
  expect(endingAddress.value).toBe('');
  expect(minmax.value).toBe('');
  expect(variance.value).toBe('');

});


test('Checking the state of the application after reset button is clicked - every input should be set to null string', () => {
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
    <button type="button" id="reset">Reset</button>
    
    
  `;
  //require('../src/frontend/script.js');

  const startingAddress = document.getElementById('startingAddress');
  const endingAddress = document.getElementById('endingAddress');
  const minmax = document.getElementById('minmax');
  const variance = document.getElementById('variance');
  const reset = document.getElementById('reset')
    
  reset.click();
  
  expect(startingAddress.value).toBe('');
  expect(endingAddress.value).toBe('');
  expect(minmax.value).toBe('');
  expect(variance.value).toBe('');

});

