from __future__ import annotations

import math

from .full_heterogeneity import (
    FullHeterogeneityConfig,
    cubic_coefficients_full,
    optimal_contraction_factor_full,
    regularity_parameters,
)


def regularity_shape_coordinates(
    config: FullHeterogeneityConfig,
) -> tuple[float, float]:
    """Return the inherited Empirical Law 4.3 shape coordinates K1 and K2.

    The two-agent K1 expression can be written as a weighted second moment of
    q_i=(L_i-mu_i)/(L_i+mu_i), while K2 is the square of the corresponding
    weighted mean. Their difference is therefore a nonnegative weighted
    variance.
    """
    config.validate()
    L1, L2, mu1, mu2 = regularity_parameters(config)
    sigma1, sigma2 = L1 + mu1, L2 + mu2
    delta1, delta2 = L1 - mu1, L2 - mu2
    sigma_sum = sigma1 + sigma2

    k1 = (delta1 * delta1 / sigma1 + delta2 * delta2 / sigma2) / sigma_sum
    k2 = ((delta1 + delta2) / sigma_sum) ** 2
    return k1, k2


def invariant_k2(kappa_bar: float) -> float:
    """Closed-form K2 under fixed arithmetic means.

    Since sum_i Delta_i = 2(L_bar-mu_bar) and sum_i Sigma_i =
    2(L_bar+mu_bar), K2 depends only on kappa_bar=L_bar/mu_bar and not on
    either heterogeneity ratio.
    """
    if kappa_bar < 1.0:
        raise ValueError("kappa_bar must satisfy kappa_bar >= 1")
    return ((kappa_bar - 1.0) / (kappa_bar + 1.0)) ** 2


def mismatch_gap_closed_form(
    tau_L: float,
    tau_mu: float,
    kappa_bar: float,
) -> float:
    """Return the exact controlled-path identity K1-K2.

    For a=tau_L, b=tau_mu, and k=kappa_bar,

      K1-K2 = 4 k^2 (a-b)^2 /
              [(k+1)^2 (a+b k+k+1) (a b k+a b+a k+b)].

    The expression is nonnegative and vanishes exactly when tau_L=tau_mu.
    """
    if not (0.0 < tau_L <= 1.0):
        raise ValueError("tau_L must lie in (0,1]")
    if not (0.0 < tau_mu <= 1.0):
        raise ValueError("tau_mu must lie in (0,1]")
    if kappa_bar < 1.0:
        raise ValueError("kappa_bar must satisfy kappa_bar >= 1")

    a = tau_L
    b = tau_mu
    k = kappa_bar
    denominator = (
        (k + 1.0) ** 2
        * (a + b * k + k + 1.0)
        * (a * b * k + a * b + a * k + b)
    )
    return 4.0 * k * k * (a - b) ** 2 / denominator


def weighted_shape_variance(config: FullHeterogeneityConfig) -> float:
    """Return the weighted variance representation of K1-K2."""
    config.validate()
    L1, L2, mu1, mu2 = regularity_parameters(config)
    sigma1, sigma2 = L1 + mu1, L2 + mu2
    q1 = (L1 - mu1) / sigma1
    q2 = (L2 - mu2) / sigma2
    sigma_sum = sigma1 + sigma2
    w1, w2 = sigma1 / sigma_sum, sigma2 / sigma_sum
    mean_q = w1 * q1 + w2 * q2
    return w1 * (q1 - mean_q) ** 2 + w2 * (q2 - mean_q) ** 2


def admissible_tau_mu_bounds(
    tau_L: float,
    kappa_bar: float,
) -> tuple[float, float]:
    """Analytic tau_mu bounds implied by mu_i <= L_i.

    The result is intersected with the natural ratio interval [0,1]. Values
    strictly inside the returned interval are admissible; endpoints may be
    equality cases.
    """
    if not (0.0 < tau_L <= 1.0):
        raise ValueError("tau_L must lie in (0,1]")
    if kappa_bar < 1.0:
        raise ValueError("kappa_bar must satisfy kappa_bar >= 1")

    a = tau_L
    k = kappa_bar

    lower = max(0.0, (1.0 + a - k) / k)
    denominator = 1.0 - (k - 1.0) * a
    if denominator <= 0.0:
        upper = 1.0
    else:
        upper = min(1.0, k * a / denominator)
    return lower, upper


def cubic_discriminant_full(config: FullHeterogeneityConfig) -> float:
    """Return the discriminant of the inherited monic cubic."""
    a, b, c, d = cubic_coefficients_full(config)
    return float(
        18.0 * a * b * c * d
        - 4.0 * b**3 * d
        + b * b * c * c
        - 4.0 * a * c**3
        - 27.0 * a * a * d * d
    )


def k1_root_sensitivity(config: FullHeterogeneityConfig) -> float:
    """Implicit derivative d rho_star / d K1 at the selected largest root.

    For Q(rho,K1)=0, partial_Q/partial_K1 = r*s*rho*(s-rho). Hence

      d rho / d K1 = r*s*rho*(rho-s) / Q'(rho).

    A positive value means increasing the K1 mismatch coordinate worsens the
    contraction factor locally. Degenerate roots are rejected explicitly.
    """
    config.validate()
    rho = optimal_contraction_factor_full(config)
    s = math.sqrt(config.epsilon)
    r = (1.0 - s) ** 2 / (1.0 + s)
    coeffs = cubic_coefficients_full(config)
    q_prime = 3.0 * rho * rho + 2.0 * coeffs[1] * rho + coeffs[2]
    if abs(q_prime) <= 1e-14:
        raise RuntimeError("selected empirical cubic root is degenerate")
    return r * s * rho * (rho - s) / q_prime
