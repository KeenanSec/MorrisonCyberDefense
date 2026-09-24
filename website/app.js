/**
 * MORRISON CYBER DEFENSE LLC — Interactive Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const mobileToggle = document.getElementById('mobile-toggle');
  const mainNav = document.getElementById('main-nav');

  if (mobileToggle && mainNav) {
    mobileToggle.addEventListener('click', () => {
      mainNav.classList.toggle('open');
    });

    // Close menu when clicking links
    mainNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('open');
      });
    });
  }

  // ==========================================
  // Interactive 60-Second Cyber Insurance Quiz
  // ==========================================
  const questions = document.querySelectorAll('.quiz-question');
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const progressFill = document.getElementById('progress-fill');
  const quizResults = document.getElementById('quiz-results');
  const quizNav = document.getElementById('quiz-nav');

  let currentStep = 1;
  const totalQuestions = questions.length;
  const answers = {};

  function updateQuestion() {
    questions.forEach(q => {
      const qNum = parseInt(q.getAttribute('data-q'), 10);
      if (qNum === currentStep) {
        q.classList.add('active');
      } else {
        q.classList.remove('active');
      }
    });

    // Progress bar update
    const progressPercent = (currentStep / totalQuestions) * 100;
    progressFill.style.width = `${progressPercent}%`;

    // Button states
    if (currentStep === 1) {
      prevBtn.style.display = 'none';
    } else {
      prevBtn.style.display = 'inline-flex';
    }

    if (answers[`q${currentStep}`]) {
      nextBtn.disabled = false;
    } else {
      nextBtn.disabled = true;
    }

    if (currentStep === totalQuestions) {
      nextBtn.textContent = 'Calculate My Score →';
    } else {
      nextBtn.textContent = 'Next Question';
    }
  }

  // Handle Option Clicks
  questions.forEach(q => {
    const qNum = q.getAttribute('data-q');
    const options = q.querySelectorAll('.q-option');

    options.forEach(opt => {
      opt.addEventListener('click', () => {
        options.forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');

        const input = opt.querySelector('input[type="radio"]');
        if (input) {
          input.checked = true;
          answers[`q${qNum}`] = input.value;
          nextBtn.disabled = false;
        }
      });
    });
  });

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentStep < totalQuestions) {
        currentStep++;
        updateQuestion();
      } else {
        calculateResults();
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentStep > 1) {
        currentStep--;
        updateQuestion();
      }
    });
  }

  function calculateResults() {
    // Hide questions and nav
    questions.forEach(q => q.classList.remove('active'));
    quizNav.style.display = 'none';
    quizResults.style.display = 'block';

    let totalPoints = 0;
    Object.values(answers).forEach(val => {
      if (val === 'pass') totalPoints += 20;
      else if (val === 'medium') totalPoints += 10;
      else if (val === 'fail') totalPoints += 0;
    });

    const scoreNumber = document.getElementById('score-number');
    const resultsHeadline = document.getElementById('results-headline');
    const resultsSummary = document.getElementById('results-summary');
    const resultsRec = document.getElementById('results-recommendation');
    const circle = document.querySelector('.results-score-circle');

    scoreNumber.textContent = `${totalPoints}%`;

    if (totalPoints >= 80) {
      circle.style.borderColor = '#10B981';
      circle.style.boxShadow = '0 0 25px rgba(16, 185, 129, 0.35)';
      resultsHeadline.textContent = 'Strong Posture — Ready for Underwriter Attestation';
      resultsSummary.textContent = 'Your Microsoft 365 environment exhibits strong baseline security controls aligned with current cyber insurance requirements.';
      resultsRec.innerHTML = '<strong>Recommended Action:</strong> Book our <strong>$2,500 Diagnostic Review</strong> to generate an official NIST CSF 2.0 posture verification report that your leadership can submit directly to insurance underwriters and general contractors.';
    } else if (totalPoints >= 50) {
      circle.style.borderColor = '#F59E0B';
      circle.style.boxShadow = '0 0 25px rgba(245, 158, 11, 0.35)';
      resultsHeadline.textContent = 'Moderate Vulnerability — High Risk of Policy Exclusions';
      resultsSummary.textContent = 'You have partial protections in place, but gaps in email authentication (DMARC), 24/7 EDR, or MFA enforcement could trigger policy renewal cancellations or significant rate hikes.';
      resultsRec.innerHTML = '<strong>Recommended Action:</strong> Schedule a diagnostic review. Our <strong>100% Roll-In Credit</strong> ensures that 100% of your $2,500 audit fee rolls directly into our <strong>M365 Defense Sprint</strong> to eliminate these specific gaps before your renewal window closes.';
    } else {
      circle.style.borderColor = '#EF4444';
      circle.style.boxShadow = '0 0 25px rgba(239, 68, 68, 0.35)';
      resultsHeadline.textContent = 'Critical Gaps Detected — High Probability of Claim Rejection';
      resultsSummary.textContent = 'Your organization is vulnerable to Business Email Compromise (BEC), wire diversion, and ransomware. Most commercial cyber insurers will reject claims if these fundamental controls are absent.';
      resultsRec.innerHTML = '<strong>Immediate Recommendation:</strong> Request an urgent 15-minute diagnostic consultation below. We can map out a 10-day remediation plan to deploy Phishing-Resistant MFA, DMARC <code>p=reject</code>, and Huntress 24/7 MDR threat isolation.';
    }
  }

  // ==========================================
  // Client Intake Form Handler
  // ==========================================
  const intakeForm = document.getElementById('intake-form');
  const formFeedback = document.getElementById('form-feedback');
  const submitBtn = document.getElementById('submit-btn');

  if (intakeForm) {
    intakeForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('full-name').value.trim();
      const company = document.getElementById('company-name').value.trim();
      const email = document.getElementById('business-email').value.trim();
      const seats = document.getElementById('seat-count').value;
      const concern = document.getElementById('primary-concern').value;

      submitBtn.disabled = true;
      submitBtn.textContent = 'Routing to Principal Architect...';

      // Simulate quick secure client intake
      setTimeout(() => {
        submitBtn.style.display = 'none';
        formFeedback.className = 'form-feedback success';
        formFeedback.innerHTML = `
          <strong>Thank you, ${name}!</strong><br>
          Your scoping request for <strong>${company}</strong> (${seats} seats) has been securely dispatched to our partners. We will respond to <strong>${email}</strong> within our 4-hour business SLA.
        `;
        intakeForm.reset();
      }, 700);
    });
  }
});
