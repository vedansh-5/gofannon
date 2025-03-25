const { readFileSync, writeFileSync, mkdirSync } = require('fs');
const { Octokit } = require('@octokit/rest');

// Initialize Octokit
const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN
});

// Load points configuration
const pointsConfig = JSON.parse(
    readFileSync('.github/points_config.json', 'utf8')
);

// Get only closed PRs
async function getClosedPRs() {
    try {
        return await octokit.paginate(octokit.rest.pulls.list, {
            owner: process.env.REPO_OWNER,
            repo: process.env.REPO_NAME,
            state: 'closed',
            per_page: 100
        });
    } catch (error) {
        console.error('Error fetching closed PRs:', error);
        throw error;
    }
}

// Calculate scores based only on closed PRs
async function calculateScores() {
    const closedPRs = await getClosedPRs();
    const scores = {};

    closedPRs.forEach(pr => {
        // Only count merged PRs or specifically closed ones
        if (pr.user && pr.user.type === 'User' && !pr.user.login.includes('[bot]')) {
            const user = pr.user.login;
            const labels = pr.labels.map(l => l.name);

            labels.forEach(label => {
                scores[user] = (scores[user] || 0) + (pointsConfig[label] || 0);
            });
        }
    });

    return Object.entries(scores)
        .sort(([,a], [,b]) => b - a)
        .map(([user, score]) => ({ user, score }));
}

// Generate markdown table
function generateMarkdown(scores) {
    let md = '---\nlayout: leaderboard\ntitle: Leaderboard\n---\n| Player | Score |\n| :--- | ---: |\n';
    scores.forEach(({ user, score }) => {
        md += `| [@${user}](https://github.com/${user}) | ${score} |\n`;
    });
    return md;
}

// Main execution
(async () => {
    try {
        const scores = await calculateScores();
        const markdown = generateMarkdown(scores);
        mkdirSync('website', { recursive: true });
        writeFileSync('website/leaderboard.md', markdown);
        console.log('Successfully updated leaderboard with closed PRs only!');
    } catch (error) {
        console.error('Error updating leaderboard:', error);
        process.exit(1);
    }
})();