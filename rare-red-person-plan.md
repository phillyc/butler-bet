# Rare Red Person Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a single-file HTML game with infinite vertical scroll of bathroom-sign people icons, where 1 in 10,000 is red and triggers a modal.

**Architecture:** Single index.html with inline CSS/JS. Generate rows of icons on-demand, pre-generate chunks to avoid lag. Fixed header displays "You don't have it".

**Tech Stack:** Vanilla HTML/CSS/JS, no dependencies. Deploy to GitHub Pages.

---

### Task 1: Create GitHub Repository

**Objective:** Set up the repo for GitHub Pages deployment.

**Files:**
- Create: `rare-red-person/index.html`
- Create: GitHub repository `nofacespoker/rare-red-person`

**Step 1: Create local directory and initialize git**

```bash
mkdir -p rare-red-person
cd rare-red-person
git init
git config user.name "Phil"
git config user.email "phil@cariou.io"
```

**Step 2: Create GitHub repository**

Run the GitHub CLI command:
```bash
gh repo create nofacespoker/rare-red-person --public --source=. --remote=upstream --push
```

If `gh` is not available, manually create via:
1. Go to https://github.com/new
2. Repository name: `rare-red-person`
3. Public
4. Don't add README (we'll push ours)
5. After creation, run:
```bash
git add index.html
git commit -m "feat: initial commit with game"
git push -u origin main
```

**Step 3: Enable GitHub Pages**

1. Go to repo Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/ (root)`
4. Save

**Step 4: Verify deployment**

Visit: `https://nofacespoker.github.io/rare-red-person/`
Expected: Should show "404 Not Found" until we push index.html

**Step 5: Commit and push**

```bash
git add .
git commit -m "setup: initialize repository for rare red person game"
git push
```

---

### Task 2: Create HTML Structure

**Objective:** Build the basic HTML skeleton with header and main container.

**Files:**
- Create: `rare-red-person/index.html`

**Step 1: Write the HTML file**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>You Don't Have It</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: white;
      overflow-x: hidden;
    }

    .header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      font-weight: 600;
      z-index: 100;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .container {
      margin-top: 60px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-height: calc(100vh - 60px);
    }

    .row {
      display: flex;
      justify-content: center;
      gap: 15px;
    }

    .person {
      width: 50px;
      height: 50px;
      background: black;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
    }

    .modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.6);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }

    .modal-overlay.show {
      display: flex;
    }

    .modal {
      background: white;
      padding: 30px;
      border-radius: 12px;
      max-width: 80%;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .modal p {
      font-size: 18px;
      line-height: 1.5;
      margin-bottom: 20px;
    }

    .modal button {
      background: black;
      color: white;
      border: none;
      padding: 12px 24px;
      font-size: 16px;
      border-radius: 8px;
      cursor: pointer;
    }

    .modal button:hover {
      opacity: 0.8;
    }
  </style>
</head>
<body>
  <div class="header">You don't have it</div>
  <div class="container" id="container"></div>

  <div class="modal-overlay" id="modal">
    <div class="modal">
      <p>This is so rare, look how far you had to scroll!</p>
      <button id="closeModal">Awesome</button>
    </div>
  </div>

  <script>
    // JavaScript will be added here
  </script>
</body>
</html>
```

**Step 2: Verify the file**

Check the content:
```bash
cat index.html
```

**Step 3: Commit and push**

```bash
git add index.html
git commit -m "feat: add HTML structure with header, container, and modal"
git push
```

**Step 4: Verify in browser**

Visit the GitHub Pages URL and verify:
- Header displays "You don't have it"
- White background
- Container is visible but empty (no rows yet)

---

### Task 3: Generate People Icons

**Objective:** Create JavaScript to generate rows of people icons with 1 in 10,000 red probability.

**Files:**
- Modify: `rare-red-person/index.html`

**Step 1: Add JavaScript to generate icons**

Add this to the `<script>` tag in `index.html`:

```javascript
const CONTAINER = document.getElementById('container');
const MODAL = document.getElementById('modal');
const CLOSE_MODAL = document.getElementById('closeModal');
const PEOPLE_PER_ROW = 5;
const RARE_CHANCE = 1 / 10000;
const CHUNK_SIZE = 100; // Generate 100 rows at a time
const SCROLL_THRESHOLD = 50; // Generate more when within 50px of bottom

let totalRows = 0;
let rowsOnScreen = 0;

function createPersonIcon(isRare = false) {
  const person = document.createElement('div');
  person.className = 'person';
  person.textContent = '🚹'; // Bathroom sign male icon
  if (isRare) {
    person.style.background = 'red';
    person.dataset.isRare = 'true';
  }
  return person;
}

function createRow(rowIndex) {
  const row = document.createElement('div');
  row.className = 'row';

  for (let i = 0; i < PEOPLE_PER_ROW; i++) {
    const isRare = Math.random() < RARE_CHANCE;
    const person = createPersonIcon(isRare);
    row.appendChild(person);
  }

  return row;
}

function addRows(count) {
  for (let i = 0; i < count; i++) {
    const row = createRow(totalRows);
    CONTAINER.appendChild(row);
    totalRows++;
    rowsOnScreen++;
  }
}

// Initial render
addRows(CHUNK_SIZE);
```

**Step 2: Verify icons appear**

Refresh the page in browser:
- Should see 100 rows of 5 black people icons each
- Layout is centered horizontally
- Scroll down to see more icons

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add people icon generation with 1-in-10k rarity"
git push
```

---

### Task 4: Implement Infinite Scroll

**Objective:** Add scroll detection to generate more rows when user scrolls near bottom.

**Files:**
- Modify: `rare-red-person/index.html`

**Step 1: Add scroll event listener**

Add this to the `<script>` tag, after the existing code:

```javascript
function checkScroll() {
  const scrollPosition = window.scrollY + window.innerHeight;
  const documentHeight = document.body.offsetHeight;

  if (documentHeight - scrollPosition < SCROLL_THRESHOLD) {
    addRows(CHUNK_SIZE);
  }
}

window.addEventListener('scroll', checkScroll);
```

**Step 2: Test scroll behavior**

1. Scroll down page slowly
2. Watch as new rows appear when near bottom
3. Scroll up and down - should generate continuously

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add infinite scroll generation"
git push
```

---

### Task 5: Add Rare Person Modal Trigger

**Objective:** When user clicks a red person, show the modal with scroll count.

**Files:**
- Modify: `rare-red-person/index.html`

**Step 1: Add click handler for rare persons**

Add this to the `<script>` tag:

```javascript
// Modal logic
let modalScrollCount = 0;

MODAL.addEventListener('click', () => {
  MODAL.classList.remove('show');
});

CLOSE_MODAL.addEventListener('click', () => {
  MODAL.classList.remove('show');
});

// Track rare persons
function checkForRarePersons() {
  const rarePersons = document.querySelectorAll('.person[data-is-rare="true"]');
  
  rarePersons.forEach(person => {
    person.style.cursor = 'pointer';
    person.addEventListener('click', () => {
      if (modalScrollCount === 0) {
        modalScrollCount = totalRows;
      }
      MODAL.classList.add('show');
      
      // Update message with scroll count
      const modal = document.querySelector('.modal');
      modal.innerHTML = `
        <p style="font-size: 20px; font-weight: 600; margin-bottom: 20px;">
          This is so rare!
        </p>
        <p style="font-size: 16px; color: #666; margin-bottom: 30px;">
          You had to scroll <strong>${modalScrollCount.toLocaleString()}</strong> rows to find it!
        </p>
        <button id="closeModal">${modalScrollCount > 1000 ? 'WOW' : 'Awesome'}</button>
      `;
      
      // Re-bind close button
      document.getElementById('closeModal').addEventListener('click', () => {
        MODAL.classList.remove('show');
      });
    });
  });
}

// Check for rare persons periodically
setInterval(checkForRarePersons, 500);
```

**Step 2: Test rare person trigger**

1. Scroll through the icons
2. When you see a red person, click it
3. Modal should appear with your scroll count

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add rare person click handler with modal"
git push
```

---

### Task 6: Optimize Performance

**Objective:** Clean up old rows when they're off-screen to prevent memory bloat.

**Files:**
- Modify: `rare-red-person/index.html`

**Step 1: Add row cleanup logic**

Replace the `addRows` function and add cleanup:

```javascript
const VIEWPORT_ROWS = Math.ceil(window.innerHeight / 60); // Approximate row height
const MAX_ROWS_TO_KEEP = VIEWPORT_ROWS + 50;

function addRows(count) {
  const startRow = totalRows;
  for (let i = 0; i < count; i++) {
    const row = createRow(totalRows);
    CONTAINER.appendChild(row);
    totalRows++;
  }
  
  // Clean up old rows
  cleanupOldRows();
}

function cleanupOldRows() {
  const rows = CONTAINER.children;
  const rowsToRemove = rows.length - MAX_ROWS_TO_KEEP;
  
  if (rowsToRemove > 0) {
    for (let i = 0; i < rowsToRemove; i++) {
      CONTAINER.removeChild(rows[0]);
    }
  }
}
```

**Step 2: Commit**

```bash
git add index.html
git commit -m "perf: add row cleanup to prevent memory bloat"
git push
```

---

### Task 7: Final Polish and Verification

**Objective:** Review the complete game and ensure everything works smoothly.

**Files:**
- Modify: `rare-red-person/index.html`

**Step 1: Add final CSS polish**

Add to the `<style>` section:

```css
.modal-overlay.show ~ .header {
  opacity: 0.5;
}

.person:hover {
  transform: scale(1.1);
  transition: transform 0.1s;
}
```

**Step 2: Final verification checklist**

Visit the GitHub Pages URL and verify:
- [ ] Header stays fixed at top
- [ ] Infinite scroll works smoothly
- [ ] 5 people per row, centered
- [ ] Rare red person appears occasionally
- [ ] Clicking red person shows modal
- [ ] Modal shows scroll count
- [ ] Performance is smooth (no lag when scrolling)
- [ ] Mobile layout looks good (test on phone)

**Step 3: Final commit**

```bash
git add index.html
git commit -m "style: add hover effects and polish"
git push
```

**Step 4: Test on mobile**

Visit the URL on your phone:
- Verify layout is mobile-friendly
- Test scroll behavior
- Verify modal appears correctly

---

## Plan Complete

Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?
