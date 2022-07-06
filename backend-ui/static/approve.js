async function approve(entitlement_id) {
    try {
      // const token = await firebase.auth().currentUser.getIdToken();
      //no auth because the entire site needs to be secured behind IAP
      const response = await fetch('{URL_PREFIX}/approve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({entitlement_id})
      });
      if (response.ok) {
        const text = await response.json();
        console.log(text)
        // window.alert(text);
        window.location.reload();
      }
      else {
        window.alert('Something went wrong... Please try again!');
      }
    } catch (err) {
      console.log(`Error when submitting approval: ${err}`);
      window.alert('Something went wrong... Please try again!');
    }
}

async function reject(entitlement_id) {
    try {
      // const token = await firebase.auth().currentUser.getIdToken();
      //no auth because the entire site needs to be secured behind IAP
      const response = await fetch('{URL_PREFIX}/reject', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({entitlement_id})
      });
      if (response.ok) {
        const text = await response.json();
        console.log(text)
        // window.alert(text);
        window.location.reload();
      }
      else {
        window.alert('Something went wrong... Please try again!');
      }
    } catch (err) {
      console.log(`Error when submitting rejection: ${err}`);
      window.alert('Something went wrong... Please try again!');
    }
}

// function go() {
//   console.log('here we go')
//   const elem = document.querySelector('select')
//   const instance = M.FormSelect.getInstance(elem);
//   const items = instance.getSelectedValues();
//   console.log(items)
//   open(`http://localhost:8080?state=${items[0]}`, "window")
// }