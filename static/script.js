document.getElementById('animeForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent page reload
    let animeName = document.getElementById('animeName').value;

    fetch(`/search_anime?anime=${animeName}`)
        .then(response => response.json())
        .then(data => {
            let resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';  // Clear previous results

            if (data.data.length === 0) {
                // No results found
                resultsDiv.innerHTML = '<p>No results found. Please check the spelling or try another search.</p>';
            } else {
                // Display the search results
                data.data.forEach(anime => {
                    let animeDiv = document.createElement('div');
                    animeDiv.innerHTML = `
                        <h3>${anime.title}</h3>
                        <img src="${anime.images.jpg.image_url}" alt="${anime.title}" width="100">
                        <p>${anime.synopsis}</p>
                        <button onclick="addToWatchlist('${anime.title}')">Add to Watchlist</button>
                    `;
                    resultsDiv.appendChild(animeDiv);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results').innerHTML = '<p>An error occurred. Please try again later.</p>';
        });
};
