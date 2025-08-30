const axios = require('axios');

class JiraClient {
  constructor(config) {
    this.baseUrl = config.baseUrl;
    this.email = config.email;
    this.apiToken = config.apiToken;
    
    // Create axios instance with auth
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      auth: {
        username: this.email,
        password: this.apiToken,
      },
    });

    // Cache for storing fetched tickets
    this.ticketCache = new Map();
  }

  async getTicket(ticketId) {
    // Check cache first
    if (this.ticketCache.has(ticketId)) {
      console.log(`Returning cached ticket: ${ticketId}`);
      return this.ticketCache.get(ticketId);
    }

    try {
      console.log(`Fetching JIRA ticket: ${ticketId}`);
      
      const response = await this.client.get(`/rest/api/2/issue/${ticketId}`, {
        params: {
          expand: 'renderedFields,comments,issuelinks,subtasks',
        },
      });

      const ticket = response.data;
      
      // Cache the ticket
      this.ticketCache.set(ticketId, ticket);
      
      return ticket;
    } catch (error) {
      if (error.response?.status === 404) {
        console.warn(`JIRA ticket not found: ${ticketId}`);
        return null;
      }
      console.error(`Error fetching JIRA ticket ${ticketId}:`, error.message);
      throw error;
    }
  }

  async getLinkedIssues(ticketId) {
    try {
      const ticket = await this.getTicket(ticketId);
      if (!ticket) return [];

      const linkedIssues = [];
      
      // Get issue links
      if (ticket.fields.issuelinks) {
        ticket.fields.issuelinks.forEach(link => {
          if (link.outwardIssue) {
            linkedIssues.push({
              key: link.outwardIssue.key,
              type: link.type.name,
              direction: 'outward',
              summary: link.outwardIssue.fields.summary,
            });
          }
          if (link.inwardIssue) {
            linkedIssues.push({
              key: link.inwardIssue.key,
              type: link.type.name,
              direction: 'inward',
              summary: link.inwardIssue.fields.summary,
            });
          }
        });
      }

      // Get subtasks
      if (ticket.fields.subtasks) {
        ticket.fields.subtasks.forEach(subtask => {
          linkedIssues.push({
            key: subtask.key,
            type: 'Subtask',
            direction: 'subtask',
            summary: subtask.fields.summary,
          });
        });
      }

      // Get parent (if this is a subtask)
      if (ticket.fields.parent) {
        linkedIssues.push({
          key: ticket.fields.parent.key,
          type: 'Parent',
          direction: 'parent',
          summary: ticket.fields.parent.fields.summary,
        });
      }

      return linkedIssues;
    } catch (error) {
      console.error(`Error fetching linked issues for ${ticketId}:`, error.message);
      return [];
    }
  }

  async searchTickets(jql) {
    try {
      console.log(`Searching JIRA with JQL: ${jql}`);
      
      const response = await this.client.get('/rest/api/2/search', {
        params: {
          jql,
          maxResults: 50,
          fields: 'summary,status,priority,description,comment,issuelinks,subtasks',
        },
      });

      return response.data.issues;
    } catch (error) {
      console.error('Error searching JIRA:', error.message);
      throw error;
    }
  }

  async getTicketComments(ticketId) {
    try {
      const ticket = await this.getTicket(ticketId);
      if (!ticket) return [];

      return ticket.fields.comment?.comments || [];
    } catch (error) {
      console.error(`Error fetching comments for ${ticketId}:`, error.message);
      return [];
    }
  }

  async addComment(ticketId, comment) {
    try {
      console.log(`Adding comment to JIRA ticket: ${ticketId}`);
      
      const response = await this.client.post(
        `/rest/api/2/issue/${ticketId}/comment`,
        {
          body: comment,
        }
      );

      return response.data;
    } catch (error) {
      console.error(`Error adding comment to ${ticketId}:`, error.message);
      throw error;
    }
  }

  async updateTicketStatus(ticketId, transitionId) {
    try {
      console.log(`Updating JIRA ticket status: ${ticketId}`);
      
      const response = await this.client.post(
        `/rest/api/2/issue/${ticketId}/transitions`,
        {
          transition: {
            id: transitionId,
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error(`Error updating status for ${ticketId}:`, error.message);
      throw error;
    }
  }

  async getTransitions(ticketId) {
    try {
      const response = await this.client.get(
        `/rest/api/2/issue/${ticketId}/transitions`
      );

      return response.data.transitions;
    } catch (error) {
      console.error(`Error fetching transitions for ${ticketId}:`, error.message);
      throw error;
    }
  }

  async linkIssues(sourceTicketId, targetTicketId, linkType = 'Relates') {
    try {
      console.log(`Linking JIRA tickets: ${sourceTicketId} -> ${targetTicketId}`);
      
      const response = await this.client.post('/rest/api/2/issueLink', {
        type: {
          name: linkType,
        },
        inwardIssue: {
          key: sourceTicketId,
        },
        outwardIssue: {
          key: targetTicketId,
        },
      });

      return response.data;
    } catch (error) {
      console.error(`Error linking tickets ${sourceTicketId} to ${targetTicketId}:`, error.message);
      throw error;
    }
  }

  async getTicketsByPR(prUrl) {
    // Search for tickets that mention this PR URL
    const jql = `text ~ "${prUrl}" ORDER BY updated DESC`;
    return this.searchTickets(jql);
  }

  async getRecentTicketsForRepository(repositoryName, daysBack = 7) {
    const date = new Date();
    date.setDate(date.getDate() - daysBack);
    const formattedDate = date.toISOString().split('T')[0];

    const jql = `text ~ "${repositoryName}" AND updated >= ${formattedDate} ORDER BY updated DESC`;
    return this.searchTickets(jql);
  }

  // Helper method to extract structured information from ticket
  extractTicketMetadata(ticket) {
    const metadata = {
      key: ticket.key,
      summary: ticket.fields.summary,
      status: ticket.fields.status?.name,
      priority: ticket.fields.priority?.name,
      type: ticket.fields.issuetype?.name,
      assignee: ticket.fields.assignee?.displayName,
      reporter: ticket.fields.reporter?.displayName,
      created: ticket.fields.created,
      updated: ticket.fields.updated,
      labels: ticket.fields.labels || [],
      components: ticket.fields.components?.map(c => c.name) || [],
      fixVersions: ticket.fields.fixVersions?.map(v => v.name) || [],
      epicLink: ticket.fields.customfield_10001, // Adjust field ID based on JIRA config
    };

    // Extract custom fields that might contain acceptance criteria
    const acceptanceCriteriaFields = [
      'customfield_10100', // Common field for AC
      'customfield_10101',
      'customfield_10102',
    ];

    for (const field of acceptanceCriteriaFields) {
      if (ticket.fields[field]) {
        metadata.acceptanceCriteria = ticket.fields[field];
        break;
      }
    }

    return metadata;
  }

  // Clear the ticket cache
  clearCache() {
    this.ticketCache.clear();
    console.log('JIRA ticket cache cleared');
  }

  // Get cache statistics
  getCacheStats() {
    return {
      size: this.ticketCache.size,
      tickets: Array.from(this.ticketCache.keys()),
    };
  }
}

module.exports = { JiraClient };
