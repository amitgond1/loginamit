document.getElementById('generate-btn').addEventListener('click', function () {
    const difficulty = document.getElementById('difficulty').value;

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: difficulty }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const questionSection = document.getElementById('question-section');
                questionSection.classList.remove('hidden');
                document.getElementById('question').textContent = data.question;

                // Apply smooth animation
                questionSection.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    questionSection.style.transform = 'scale(1)';
                }, 500);
            }
        })
        .catch(err => console.error('Error:', err));
});
