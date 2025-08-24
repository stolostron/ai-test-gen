# AI Systems Suite - Extensions

## 🔧 Adding New Applications

Follow the proven isolation pattern:

1. **Create App Directory**: `apps/your-app-name/`
2. **Add App Config**: `.app-config` with unique name and AI service prefix
3. **Create Isolated CLAUDE.md**: Include isolation headers and self-contained logic
4. **Implement AI Services**: Use unique prefix for all service files
5. **Verify Isolation**: Test independence using verification guidelines
6. **Auto-Registration**: Smart Proxy Router automatically discovers and registers the new app
7. **Global Access**: New app immediately available via `/your-app-name` commands from root

**Template Available**: `shared/templates/app-extension-guide.md` provides complete step-by-step instructions.

**Technical Details**: See `shared/docs/smart-router-technical.md` for comprehensive implementation details, `shared/docs/ai-powered-routing-service.md` for AI routing intelligence, and `shared/docs/performance-metrics.md` for performance benchmarks.