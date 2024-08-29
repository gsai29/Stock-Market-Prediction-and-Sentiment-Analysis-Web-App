// import Dashboard from './Dashboard';

// import React, { useState } from 'react';
// import './App.css';

// function App() {
//   const [email, setEmail] = useState('');
//   const [name, setName] = useState('');
//   const [stock, setStock] = useState('');
//   const [company, setCompany] = useState('');
//   const [userData, setUserData] = useState(null);  // Adjusted for better null checking
//   const [userStatus, setUserStatus] = useState('');
//   const [searchHistory, setSearchHistory] = useState([]);
//   const [error, setError] = useState('');
//   const [analysisResults, setAnalysisResults] = useState(null);
//   const displayValue = value => value === null ? 'Data not available' : value;

//   const handleEmailSubmit = async (event) => {
//     event.preventDefault();
//     setError('');
//     try {
//       const response = await fetch('/mongodb_search_email', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({ email: email }),
//       });
//       const data = await response.json();
//       if (response.ok) {
//         setUserStatus(data.status);
//         if (data.data) { // Added check for data existence
//           setName(data.data.name);
//           setSearchHistory(data.data.history || []);
//           setUserData(data.data);
//         }
//       } else {
//         throw new Error(data.error || 'Something went wrong');
//       }
//     } catch (err) {
//       setError(err.message);
//     }
//   };

//   const handleNameSubmit = async (event) => {
//     event.preventDefault();
//     if (name.trim()) { // Ensure name is not just whitespace
//       setUserStatus('name_submitted');
//     }
//   };


//   const handleStockSubmit = async (event) => {
//     event.preventDefault();
//     const dateTime = new Date().toISOString();
  
//     let endpoint, payload;
//     if (userStatus === 'found' && userData) {
//       endpoint = '/mongodb_update';
//       payload = {
//         id: userData._id.$oid,
//         company: company,
//         dateTime: dateTime
//       };

//     } else {
//       endpoint = '/mongodb_create';
//       payload = {
//         email: email,
//         name: name,
//         company: company,
//         dateTime: dateTime
//       };
//     }
  
//     try {
//       const response = await fetch(endpoint, {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify(payload),
//       });
//       if (response.ok) {
//         console.log('Submission successful for update/create');
//         // Proceed to call insertintotable after successful update/create
//         await submitToInsertIntoTable(stock, company);
//       } else {
//         const result = await response.json();
//         throw new Error(result.error || 'Failed to update/create user details');
//       }
//     } catch (err) {
//       console.error('Error:', err);
//       setError(err.message);
//     }
//   };
  
//   const submitToInsertIntoTable = async (stock, company) => {
//     try {
//       const response = await fetch('/insertintotable', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({ nm: stock, company: company }),
//       });
//       const data = await response.json();
//       if (response.ok) {
//         setAnalysisResults(data);  // Set the data
//         console.log('Data from insertintotable:', data);
//       } else {
//         throw new Error(data.error || 'Failed to fetch analysis results');
//       }
//     } catch (err) {
//       console.error('Error fetching results:', err);
//       setError(err.message);
//     }
//   };
  
  
//   return (
//     <div className="App">
//       {analysisResults ? (
//         <Dashboard data={analysisResults} />
//       ) : (
//         <div className="App-header">
//           {userStatus === '' && (
//             <form onSubmit={handleEmailSubmit}>
//               <label htmlFor="email">Enter your Email Address:</label>
//               <input
//                 type="email"
//                 id="email"
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 required
//               />
//               <button type="submit">Submit</button>
//             </form>
//           )}
  
//           {userStatus === 'not_found' && (
//             <form onSubmit={handleNameSubmit}>
//               <label htmlFor="name">Enter your Name:</label>
//               <input
//                 type="text"
//                 id="name"
//                 value={name}
//                 onChange={(e) => setName(e.target.value)}
//                 required
//               />
//               <button type="submit">Submit</button>
//             </form>
//           )}
  
//           {(userStatus === 'found' || userStatus === 'name_submitted') && (
//             <>
//               <h2>Welcome {userStatus === 'found' ? 'Back' : ''}, {name}!</h2>
//               <form onSubmit={handleStockSubmit}>
//                 <label htmlFor="stock">Enter Stock Symbol:</label>
//                 <input
//                   type="text"
//                   id="stock"
//                   value={stock}
//                   onChange={(e) => setStock(e.target.value)}
//                   required
//                 />
//                 <label htmlFor="company">Enter Company Name:</label>
//                 <input
//                   type="text"
//                   id="company"
//                   value={company}
//                   onChange={(e) => setCompany(e.target.value)}
//                   required
//                 />
//                 <button type="submit">Submit</button>
//               </form>
//               <div className="search-history">
//                 {searchHistory.length > 0 && (
//                   <>
//                     <h3>Quick History</h3>
//                     {searchHistory.map((item, index) => (
//                       <div key={index}>{item.date} - {item.company}</div>
//                     ))}
//                   </>
//                 )}
//               </div>
//             </>
//           )}
  
//           {error && <div>Error: {error}</div>}
//         </div>
//       )}
//     </div>
//   );
  
// }

// export default App;



import Dashboard from './Dashboard';
import React, { useState } from 'react';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [stock, setStock] = useState('');
  const [company, setCompany] = useState('');
  const [userData, setUserData] = useState(null);  // Adjusted for better null checking
  const [userStatus, setUserStatus] = useState('');
  const [searchHistory, setSearchHistory] = useState([]);
  const [error, setError] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleEmailSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      const response = await fetch('/mongodb_search_email', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: email }),
      });
      const data = await response.json();
      if (response.ok) {
        setUserStatus(data.status);
        if (data.data) {
          setName(data.data.name);
          setSearchHistory(data.data.history || []);
          setUserData(data.data);
        }
      } else {
        throw new Error(data.error || 'Something went wrong');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleNameSubmit = async (event) => {
    event.preventDefault();
    if (name.trim()) {
      setUserStatus('name_submitted');
    }
  };

  const handleStockSubmit = async (event) => {
    event.preventDefault();
    const dateTime = new Date().toISOString();
    let endpoint, payload;
    if (userStatus === 'found' && userData) {
      endpoint = '/mongodb_update';
      payload = {
        id: userData._id.$oid,
        company: company,
        dateTime: dateTime
      };
    } else {
      endpoint = '/mongodb_create';
      payload = {
        email: email,
        name: name,
        company: company,
        dateTime: dateTime
      };
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
      });
      if (response.ok) {
        console.log('Submission successful for update/create');
        await submitToInsertIntoTable(stock, company);
      } else {
        const result = await response.json();
        throw new Error(result.error || 'Failed to update/create user details');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.message);
    }
  };

  const submitToInsertIntoTable = async (stock, company) => {
    try {
      const response = await fetch('/insertintotable', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ nm: stock, company: company }),
      });
      const data = await response.json();
      if (response.ok) {
        setAnalysisResults(data);
        console.log('Data from insertintotable:', data);
      } else {
        throw new Error(data.error || 'Failed to fetch analysis results');
      }
    } catch (err) {
      console.error('Error fetching results:', err);
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <div className="app-title">
        Stock Prediction and Sentiment Analysis App by Gowri Shankar Sai Manikandan,Vignesh and Shrishailya
      </div>
      {analysisResults ? (
        <Dashboard data={analysisResults} />
      ) : (
        <div className="App-header">
          {userStatus === '' && (
            <form onSubmit={handleEmailSubmit}>
              <label htmlFor="email">Enter your Email Address:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <button type="submit">Submit</button>
            </form>
          )}
          {userStatus === 'not_found' && (
            <form onSubmit={handleNameSubmit}>
              <label htmlFor="name">Enter your Name:</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
              <button type="submit">Submit</button>
            </form>
          )}
          {(userStatus === 'found' || userStatus === 'name_submitted') && (
            <>
              <h2>Welcome {userStatus === 'found' ? 'Back' : ''}, {name}!</h2>
              <form onSubmit={handleStockSubmit}>
                <label htmlFor="stock">Enter Stock Symbol:</label>
                <input
                  type="text"
                  id="stock"
                  value={stock}
                  onChange={(e) => setStock(e.target.value)}
                  required
                />
                <label htmlFor="company">Enter Company Name:</label>
                <input
                  type="text"
                  id="company"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  required
                />
                <button type="submit">Submit</button>
              </form>
              <div className="search-history">
                {searchHistory.length > 0 && (
                  <>
                    <h3>Quick History</h3>
                    {searchHistory.map((item, index) => (
                      <div key={index}>{item.date} - {item.company}</div>
                    ))}
                  </>
                )}
              </div>
            </>
          )}
          {error && <div>Error: {error}</div>}
        </div>
      )}
    </div>
  );
}

export default App;
