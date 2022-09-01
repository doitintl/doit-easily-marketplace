async function approve(entitlement_id) {
    try {
      const response = await fetch(`/v1/entitlement/${entitlement_id}/approve`, {
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

async function reject(entitlement_id, reason) {
    try {
      const response = await fetch(`/v1/entitlement/${entitlement_id}/reject`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({entitlement_id, reason})
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