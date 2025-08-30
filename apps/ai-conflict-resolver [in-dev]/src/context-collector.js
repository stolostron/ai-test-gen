const { graphql } = require('@octokit/graphql');

class ContextCollector {
  constructor({ github, jira }) {
    this.github = github;
    this.jira = jira;
  }

  async gatherContext({ repository, pullRequest, octokit }) {
    console.log('Gathering comprehensive context for conflict resolution...');
    
    const [
      jiraContext,
      githubContext,
      codeContext,
      testContext,
      teamContext,
    ] = await Promise.all([
      this.collectJiraContext(pullRequest),
      this.collectGitHubContext({ repository, pullRequest, octokit }),
      this.collectCodeContext({ repository, pullRequest, octokit }),
      this.collectTestContext({ repository, pullRequest, octokit }),
      this.collectTeamContext({ repository, pullRequest, octokit }),
    ]);

    return {
      jiraTickets: jiraContext.tickets,
      relatedPRs: githubContext.relatedPRs,
      commits: githubContext.commits,
      recentActivity: githubContext.recentActivity,
      codePatterns: codeContext.patterns,
      dependencies: codeContext.dependencies,
      testFiles: testContext.files,
      testCoverage: testContext.coverage,
      teamPreferences: teamContext.preferences,
      historicalResolutions: teamContext.historicalResolutions,
      metadata: {
        collectionTime: new Date().toISOString(),
        sources: ['jira', 'github', 'code-analysis', 'test-analysis', 'team-history'],
      },
    };
  }

  async collectJiraContext(pullRequest) {
    const tickets = [];
    
    // Extract JIRA ticket IDs from PR title and body
    const jiraPattern = /\b([A-Z]{2,}-\d+)\b/g;
    const prText = `${pullRequest.title} ${pullRequest.body || ''}`;
    const ticketIds = [...new Set(prText.match(jiraPattern) || [])];

    console.log(`Found JIRA tickets: ${ticketIds.join(', ')}`);

    // Fetch each ticket and its linked issues
    for (const ticketId of ticketIds) {
      try {
        const ticket = await this.jira.getTicket(ticketId);
        tickets.push(ticket);

        // Get linked tickets recursively (up to 2 levels deep)
        const linkedTickets = await this.getLinkedTickets(ticketId, 2);
        tickets.push(...linkedTickets);
      } catch (error) {
        console.error(`Failed to fetch JIRA ticket ${ticketId}:`, error);
      }
    }

    return {
      tickets: this.enrichJiraTickets(tickets),
    };
  }

  async getLinkedTickets(ticketId, depth) {
    if (depth <= 0) return [];
    
    const linkedTickets = [];
    
    try {
      const links = await this.jira.getLinkedIssues(ticketId);
      
      for (const link of links) {
        const linkedTicket = await this.jira.getTicket(link.key);
        linkedTickets.push(linkedTicket);
        
        // Recursively get linked tickets
        const subLinked = await this.getLinkedTickets(link.key, depth - 1);
        linkedTickets.push(...subLinked);
      }
    } catch (error) {
      console.error(`Error fetching linked tickets for ${ticketId}:`, error);
    }
    
    return linkedTickets;
  }

  enrichJiraTickets(tickets) {
    return tickets.map(ticket => ({
      key: ticket.key,
      summary: ticket.fields.summary,
      description: ticket.fields.description,
      status: ticket.fields.status.name,
      priority: ticket.fields.priority?.name,
      acceptanceCriteria: this.extractAcceptanceCriteria(ticket),
      testScenarios: this.extractTestScenarios(ticket),
      url: `${this.jira.baseUrl}/browse/${ticket.key}`,
      linkedPRs: this.extractLinkedPRs(ticket),
      comments: this.extractRelevantComments(ticket),
    }));
  }

  extractAcceptanceCriteria(ticket) {
    const description = ticket.fields.description || '';
    const acMatch = description.match(/acceptance criteria:?\s*([\s\S]*?)(?:test|scenario|given|$)/i);
    return acMatch ? acMatch[1].trim() : '';
  }

  extractTestScenarios(ticket) {
    const description = ticket.fields.description || '';
    const testMatch = description.match(/test scenario:?\s*([\s\S]*?)(?:acceptance|notes|$)/i);
    return testMatch ? testMatch[1].trim() : '';
  }

  extractLinkedPRs(ticket) {
    const prs = [];
    const description = ticket.fields.description || '';
    const comments = ticket.fields.comment?.comments || [];
    
    // Look for GitHub PR links in description and comments
    const prPattern = /github\.com\/[^\/]+\/[^\/]+\/pull\/(\d+)/g;
    const allText = description + ' ' + comments.map(c => c.body).join(' ');
    
    let match;
    while ((match = prPattern.exec(allText)) !== null) {
      prs.push(parseInt(match[1]));
    }
    
    return [...new Set(prs)];
  }

  extractRelevantComments(ticket) {
    const comments = ticket.fields.comment?.comments || [];
    
    // Filter for comments that might contain relevant technical information
    return comments
      .filter(comment => {
        const body = comment.body.toLowerCase();
        return body.includes('test') || 
               body.includes('implement') || 
               body.includes('fix') ||
               body.includes('conflict') ||
               body.includes('merge');
      })
      .map(comment => ({
        author: comment.author.displayName,
        created: comment.created,
        body: comment.body,
      }));
  }

  async collectGitHubContext({ repository, pullRequest, octokit }) {
    // Get commit history
    const { data: commits } = await octokit.pulls.listCommits({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
      per_page: 100,
    });

    // Get related PRs (PRs that touch the same files)
    const relatedPRs = await this.findRelatedPRs({
      repository,
      pullRequest,
      octokit,
    });

    // Get recent repository activity
    const recentActivity = await this.getRecentActivity({
      repository,
      octokit,
    });

    return {
      commits: commits.map(c => ({
        sha: c.sha,
        message: c.commit.message,
        author: c.commit.author.name,
        date: c.commit.author.date,
      })),
      relatedPRs,
      recentActivity,
    };
  }

  async findRelatedPRs({ repository, pullRequest, octokit }) {
    // Get files changed in this PR
    const { data: files } = await octokit.pulls.listFiles({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
    });

    const filePaths = files.map(f => f.filename);
    
    // Search for other PRs that modified these files
    const searchQuery = `repo:${repository.full_name} is:pr ${filePaths.map(f => `filename:${f}`).join(' OR ')}`;
    
    try {
      const { data: searchResults } = await octokit.search.issuesAndPullRequests({
        q: searchQuery,
        per_page: 10,
        sort: 'updated',
        order: 'desc',
      });

      return searchResults.items
        .filter(item => item.number !== pullRequest.number)
        .map(item => ({
          number: item.number,
          title: item.title,
          state: item.state,
          author: item.user.login,
          url: item.html_url,
        }));
    } catch (error) {
      console.error('Error searching for related PRs:', error);
      return [];
    }
  }

  async getRecentActivity({ repository, octokit }) {
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    try {
      const { data: recentCommits } = await octokit.repos.listCommits({
        owner: repository.owner.login,
        repo: repository.name,
        since: oneWeekAgo.toISOString(),
        per_page: 50,
      });

      return {
        recentCommitCount: recentCommits.length,
        activeContributors: [...new Set(recentCommits.map(c => c.author?.login).filter(Boolean))],
        commitFrequency: recentCommits.length / 7, // commits per day
      };
    } catch (error) {
      console.error('Error fetching recent activity:', error);
      return {
        recentCommitCount: 0,
        activeContributors: [],
        commitFrequency: 0,
      };
    }
  }

  async collectCodeContext({ repository, pullRequest, octokit }) {
    // Analyze code patterns and dependencies
    const { data: files } = await octokit.pulls.listFiles({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
    });

    const patterns = this.analyzeCodePatterns(files);
    const dependencies = await this.analyzeDependencies({
      repository,
      files,
      octokit,
    });

    return {
      patterns,
      dependencies,
    };
  }

  analyzeCodePatterns(files) {
    const patterns = {
      fileTypes: {},
      changeTypes: {
        additions: 0,
        deletions: 0,
        modifications: 0,
      },
      complexity: 'low', // This would be more sophisticated in reality
    };

    files.forEach(file => {
      // Count file types
      const ext = file.filename.split('.').pop();
      patterns.fileTypes[ext] = (patterns.fileTypes[ext] || 0) + 1;

      // Count change types
      patterns.changeTypes.additions += file.additions;
      patterns.changeTypes.deletions += file.deletions;
      
      if (file.status === 'modified') {
        patterns.changeTypes.modifications++;
      }
    });

    // Assess complexity based on changes
    const totalChanges = patterns.changeTypes.additions + patterns.changeTypes.deletions;
    if (totalChanges > 500) {
      patterns.complexity = 'high';
    } else if (totalChanges > 100) {
      patterns.complexity = 'medium';
    }

    return patterns;
  }

  async analyzeDependencies({ repository, files, octokit }) {
    const dependencies = {
      packages: [],
      internalModules: [],
      criticalFiles: [],
    };

    // Check if package.json is modified
    const packageJsonModified = files.some(f => f.filename.includes('package.json'));
    if (packageJsonModified) {
      dependencies.packages.push('package.json modified - dependency changes');
    }

    // Identify critical files (config, core modules, etc.)
    files.forEach(file => {
      if (file.filename.includes('config') || 
          file.filename.includes('core') ||
          file.filename.includes('.env')) {
        dependencies.criticalFiles.push(file.filename);
      }
    });

    return dependencies;
  }

  async collectTestContext({ repository, pullRequest, octokit }) {
    // Find test files related to the changes
    const { data: files } = await octokit.pulls.listFiles({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
    });

    const testFiles = [];
    const sourceFiles = [];

    files.forEach(file => {
      if (file.filename.includes('test') || 
          file.filename.includes('spec') ||
          file.filename.includes('cypress')) {
        testFiles.push(file.filename);
      } else if (file.filename.endsWith('.js') || 
                 file.filename.endsWith('.jsx') ||
                 file.filename.endsWith('.ts') ||
                 file.filename.endsWith('.tsx')) {
        sourceFiles.push(file.filename);
      }
    });

    // Find test files for source files
    const relatedTestFiles = this.findRelatedTestFiles(sourceFiles);
    testFiles.push(...relatedTestFiles);

    // Get test coverage if available
    const coverage = await this.getTestCoverage({
      repository,
      pullRequest,
      octokit,
    });

    return {
      files: [...new Set(testFiles)],
      coverage,
      hasTests: testFiles.length > 0,
      testToSourceRatio: testFiles.length / Math.max(sourceFiles.length, 1),
    };
  }

  findRelatedTestFiles(sourceFiles) {
    return sourceFiles.map(file => {
      const baseName = file.replace(/\.(js|jsx|ts|tsx)$/, '');
      return [
        `${baseName}.test.js`,
        `${baseName}.spec.js`,
        `${baseName}.test.ts`,
        `${baseName}.spec.ts`,
        `tests/${baseName}.js`,
        `__tests__/${baseName}.js`,
      ];
    }).flat();
  }

  async getTestCoverage({ repository, pullRequest, octokit }) {
    // This would integrate with actual coverage tools
    // For now, returning mock data
    return 85.5;
  }

  async collectTeamContext({ repository, pullRequest, octokit }) {
    // Get historical conflict resolutions
    const historicalResolutions = await this.getHistoricalResolutions({
      repository,
      octokit,
    });

    // Get team preferences based on past behavior
    const preferences = this.analyzeTeamPreferences(historicalResolutions);

    return {
      preferences,
      historicalResolutions,
    };
  }

  async getHistoricalResolutions({ repository, octokit }) {
    // Search for past conflict resolution PRs
    try {
      const { data: searchResults } = await octokit.search.issuesAndPullRequests({
        q: `repo:${repository.full_name} is:pr is:merged conflict resolution in:title`,
        per_page: 20,
        sort: 'updated',
        order: 'desc',
      });

      return searchResults.items.map(pr => ({
        number: pr.number,
        title: pr.title,
        mergedAt: pr.closed_at,
        author: pr.user.login,
        url: pr.html_url,
      }));
    } catch (error) {
      console.error('Error fetching historical resolutions:', error);
      return [];
    }
  }

  analyzeTeamPreferences(historicalResolutions) {
    // Analyze patterns in how the team has resolved conflicts
    const preferences = {
      preferredStrategies: [],
      commonPatterns: [],
      riskTolerance: 'medium',
    };

    // This would be more sophisticated in a real implementation
    if (historicalResolutions.length > 10) {
      preferences.riskTolerance = 'high'; // Team is comfortable with automated resolutions
    }

    return preferences;
  }
}

module.exports = { ContextCollector };
