# Reusable CSS Components — Spendly

Before writing new CSS, check if an existing class covers your need. These are all defined in `static/css/style.css`.

---

## Buttons

| Class | Description | When to use |
|---|---|---|
| `.btn-primary` | Filled green button | Primary CTAs outside the hero |
| `.btn-ghost` | Outlined / ghost button | Secondary actions |
| `.btn-hero` | Large black pill button | Hero section only |
| `.btn-submit` | Full-width form submit | Inside `<form>` elements |

```html
<a href="{{ url_for('register') }}" class="btn-primary">Get started</a>
<a href="#" class="btn-ghost">Learn more</a>
<a href="{{ url_for('register') }}" class="btn-hero">Create free account</a>
<button type="submit" class="btn-submit">Sign in</button>
```

---

## Auth / Form Pages

Structure for any centered form or auth page. Copy from `examples/new-auth-page.html`.

```html
<section class="auth-section">
  <div class="auth-container">
    <div class="auth-header">
      <h1 class="auth-title">Page Title</h1>
      <p class="auth-subtitle">Supporting subtitle text.</p>
    </div>

    {% if error %}
    <div class="auth-error">{{ error }}</div>
    {% endif %}

    <div class="auth-card">
      <form method="POST" action="{{ url_for('your_route') }}">

        <div class="form-group">
          <label for="email">Email address</label>
          <input type="email" id="email" name="email"
                 class="form-input" placeholder="you@example.com"
                 autofocus required>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" name="password"
                 class="form-input" required>
          <span class="form-hint">Min. 8 characters</span>
        </div>

        <button type="submit" class="btn-submit">Continue</button>
      </form>
    </div>

    <p class="auth-switch">
      Already have an account? <a href="{{ url_for('login') }}">Sign in</a>
    </p>
  </div>
</section>
```

---

## Static Content Pages (Terms / Privacy style)

Copy from `examples/new-static-page.html`.

```html
<section class="terms-page">
  <div class="terms-inner">
    <h1>Page Title</h1>
    <p class="last-updated">Last updated: May 2026</p>

    <div class="terms-section">
      <h2>Section Heading</h2>
      <p>Section body text. Keep paragraphs concise and scannable.</p>
    </div>
  </div>
</section>
```

---

## Feature Cards

Three-column grid that stacks at 900px. Add or remove `.feature-card` blocks as needed.

```html
<section class="features">
  <div class="features-inner">
    <div class="feature-card">
      <div class="feature-icon">◈</div>
      <h3 class="feature-title">Feature Name</h3>
      <p class="feature-body">Short description of the feature and its value.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">◎</div>
      <h3 class="feature-title">Feature Name</h3>
      <p class="feature-body">Short description of the feature and its value.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">◷</div>
      <h3 class="feature-title">Feature Name</h3>
      <p class="feature-body">Short description of the feature and its value.</p>
    </div>
  </div>
</section>
```

---

## CTA Section

```html
<section class="cta-section">
  <div class="cta-inner">
    <h2 class="cta-title">Ready to take control?</h2>
    <p class="cta-body">Join thousands of people who track their expenses with Spendly.</p>
    <a href="{{ url_for('register') }}" class="btn-primary">Create free account</a>
  </div>
</section>
```

---

## Form Fields (standalone)

```html
<!-- Basic field -->
<div class="form-group">
  <label for="amount">Amount</label>
  <input type="number" id="amount" name="amount"
         class="form-input" placeholder="0.00" required>
</div>

<!-- Field with hint -->
<div class="form-group">
  <label for="password">Password</label>
  <input type="password" id="password" name="password"
         class="form-input" required>
  <span class="form-hint">Min. 8 characters</span>
</div>

<!-- Select field -->
<div class="form-group">
  <label for="category">Category</label>
  <select id="category" name="category" class="form-input">
    <option value="">Select a category</option>
    <option value="food">Food</option>
    <option value="travel">Travel</option>
  </select>
</div>
```

---

## Video / Overlay Modal

HTML structure — place before `{% endblock %}`:

```html
<div id="my-modal" class="modal-overlay" aria-hidden="true">
  <div class="modal-box">
    <button class="modal-close" id="modal-close" aria-label="Close">&times;</button>
    <div class="modal-video">
      <iframe id="modal-iframe"
              data-src="https://www.youtube.com/embed/VIDEO_ID?enablejsapi=1"
              src="" frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen></iframe>
    </div>
  </div>
</div>
```

JS — place in `{% block scripts %}`:

```js
(function () {
  var modal    = document.getElementById('my-modal');
  var iframe   = document.getElementById('modal-iframe');
  var trigger  = document.getElementById('btn-trigger');
  var closeBtn = document.getElementById('modal-close');

  function openModal() {
    iframe.src = iframe.dataset.src;
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
  }
  function closeModal() {
    iframe.src = '';
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
  }

  trigger.addEventListener('click', function (e) { e.preventDefault(); openModal(); });
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
}());
```

---

## Hero Badge

Used in the hero section to show a short trust signal.

```html
<div class="hero-badge">
  <span class="hero-badge-dot"></span>
  Free to use · No credit card needed
</div>
```