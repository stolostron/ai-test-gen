#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Setup script to create necessary directories for logging and metrics
 */

const directories = [
  'logs',
  'logs/archive',
  'metrics',
  'metrics/archive'
];

function createDirectories() {
  console.log('Setting up logging and metrics directories...');
  
  directories.forEach(dir => {
    const fullPath = path.join(process.cwd(), dir);
    
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      console.log(`✓ Created directory: ${dir}`);
    } else {
      console.log(`✓ Directory already exists: ${dir}`);
    }
  });
  
  // Create .gitkeep files to ensure directories are tracked but contents are ignored
  directories.forEach(dir => {
    const gitkeepPath = path.join(process.cwd(), dir, '.gitkeep');
    if (!fs.existsSync(gitkeepPath)) {
      fs.writeFileSync(gitkeepPath, '');
      console.log(`✓ Created .gitkeep in ${dir}`);
    }
  });
  
  console.log('\n✅ Logging and metrics setup completed successfully!');
  console.log('\nNext steps:');
  console.log('1. Copy .env.example to .env and configure your settings');
  console.log('2. Run npm start to start the application');
  console.log('3. Access metrics at http://localhost:3000/api/metrics');
  console.log('4. Access analytics at http://localhost:3000/api/analytics');
}

if (require.main === module) {
  createDirectories();
}

module.exports = { createDirectories };