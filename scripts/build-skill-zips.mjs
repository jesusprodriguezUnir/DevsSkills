/**
 * Pre-build script: generates a ZIP file for each skill folder in /skills
 * and places them in /public/downloads/<skill-name>.zip
 * Also generates a skills-manifest.json with metadata for the Astro page.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import archiver from 'archiver';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const DOWNLOADS_DIR = path.join(ROOT, 'public', 'downloads');
const MANIFEST_PATH = path.join(ROOT, 'src', 'data', 'skills-manifest.json');

// Ensure output directories exist
fs.mkdirSync(DOWNLOADS_DIR, { recursive: true });
fs.mkdirSync(path.dirname(MANIFEST_PATH), { recursive: true });

/**
 * Parse YAML frontmatter from a SKILL.md file
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};
  
  const yaml = match[1];
  const result = {};
  
  // Simple YAML parser for flat key-value pairs
  for (const line of yaml.split(/\r?\n/)) {
    const kvMatch = line.match(/^(\w[\w-]*):\s*(.+)$/);
    if (kvMatch) {
      let value = kvMatch[2].trim();
      // Remove surrounding quotes
      if ((value.startsWith('"') && value.endsWith('"')) || 
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      result[kvMatch[1]] = value;
    }
  }
  
  return result;
}

/**
 * Get the body content (after frontmatter) from SKILL.md
 */
function getBody(content) {
  return content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '').trim();
}

/**
 * Auto-detect category from skill name
 */
function detectCategory(name) {
  if (name.startsWith('openup-')) return 'OpenUP';
  if (name.startsWith('dotnet-')) return '.NET Core';
  if (name.startsWith('pdf-')) return 'Utilidades';
  if (name.startsWith('skill-')) return 'Meta';
  return 'General';
}

/**
 * Count files recursively in a directory
 */
function countFiles(dir) {
  let count = 0;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isFile()) count++;
    else if (entry.isDirectory()) count += countFiles(path.join(dir, entry.name));
  }
  return count;
}

/**
 * Get total size of a directory in bytes
 */
function getDirSize(dir) {
  let size = 0;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isFile()) size += fs.statSync(full).size;
    else if (entry.isDirectory()) size += getDirSize(full);
  }
  return size;
}

/**
 * List subdirectories inside a skill folder
 */
function getSubdirs(dir) {
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(e => e.isDirectory())
    .map(e => e.name);
}

/**
 * Create a ZIP archive from a directory
 */
function zipDirectory(sourceDir, outPath) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', () => resolve(archive.pointer()));
    archive.on('error', reject);

    archive.pipe(output);
    archive.directory(sourceDir, path.basename(sourceDir));
    archive.finalize();
  });
}

// ── Main ──
async function main() {
  console.log('🔧 Building skill ZIPs and manifest...\n');

  const skillDirs = fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name)
    .sort();

  const manifest = [];

  for (const skillName of skillDirs) {
    const skillDir = path.join(SKILLS_DIR, skillName);
    const skillMdPath = path.join(skillDir, 'SKILL.md');

    if (!fs.existsSync(skillMdPath)) {
      console.log(`  ⚠ Skipping ${skillName} (no SKILL.md)`);
      continue;
    }

    const raw = fs.readFileSync(skillMdPath, 'utf-8');
    const meta = parseFrontmatter(raw);
    const body = getBody(raw);

    // Generate ZIP
    const zipPath = path.join(DOWNLOADS_DIR, `${skillName}.zip`);
    const zipSize = await zipDirectory(skillDir, zipPath);

    const entry = {
      id: skillName,
      name: meta.name || skillName,
      description: meta.description || 'Sin descripción.',
      category: detectCategory(skillName),
      license: meta.license || 'Private',
      compatibility: meta.compatibility || null,
      fileCount: countFiles(skillDir),
      rawSize: getDirSize(skillDir),
      zipSize,
      subdirs: getSubdirs(skillDir),
      body,
      downloadUrl: `/downloads/${skillName}.zip`,
    };

    manifest.push(entry);
    console.log(`  ✅ ${skillName} → ${(zipSize / 1024).toFixed(1)} KB`);
  }

  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf-8');
  console.log(`\n📦 ${manifest.length} skills processed.`);
  console.log(`📄 Manifest written to ${MANIFEST_PATH}`);
}

main().catch(err => {
  console.error('❌ Build failed:', err);
  process.exit(1);
});
