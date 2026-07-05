// this_file: namzy-rs/tests/contract.rs
//! Contract tests: determinism and output shape for the Rust port.
//!
//! The four implementations are equivalent in spirit, not bit-identical, so we
//! assert the algorithm's guarantees rather than fixed strings.

use namzy::{
    apply_rotation, generate, generate_many, Mulberry32, Options, BAD_SEAMS, ROTATIONS, STEMS,
};

fn seeded(seed: u64) -> String {
    generate(&Options { seed: Some(seed) })
}

#[test]
fn generate_is_deterministic_for_a_seed() {
    assert_eq!(seeded(42), seeded(42));
}

#[test]
fn generated_names_are_capitalized_ascii_and_short() {
    for seed in 0..500u64 {
        let name = seeded(seed);
        assert!(!name.is_empty(), "name must not be empty");
        let first = name.chars().next().unwrap();
        assert!(first.is_ascii_uppercase(), "not capitalized: {name}");
        assert!(
            name.chars().all(|c| c.is_ascii_alphabetic()),
            "non-ascii: {name}"
        );
        assert!(name.len() <= 16, "unexpectedly long: {name}");
    }
}

#[test]
fn different_seeds_usually_differ() {
    let mut names = std::collections::HashSet::new();
    for seed in 0..200u64 {
        names.insert(seeded(seed));
    }
    assert!(names.len() > 150, "too few distinct names: {}", names.len());
}

#[test]
fn generate_many_count_and_determinism() {
    let opts = Options { seed: Some(7) };
    let first = generate_many(25, &opts);
    assert_eq!(first.len(), 25);
    assert_eq!(first, generate_many(25, &Options { seed: Some(7) }));
}

#[test]
fn data_tables_are_well_formed() {
    assert!(!STEMS.is_empty());
    assert!(!ROTATIONS.is_empty());
    assert!(!BAD_SEAMS.is_empty());
    for stem in STEMS {
        assert!(
            stem.chars().all(|c| c.is_ascii_lowercase()),
            "bad stem: {stem}"
        );
    }
    for (src, dst) in ROTATIONS {
        assert!(!src.is_empty() && !dst.is_empty());
        assert_ne!(src, dst, "no-op rotation: {src}");
    }
}

#[test]
fn apply_rotation_leaves_vowel_string_untouched() {
    // Every rotation source starts with a consonant.
    assert!(ROTATIONS
        .iter()
        .all(|(src, _)| !"aeiouy".contains(&src[..1])));
    let mut rng = Mulberry32::new(0);
    assert_eq!(apply_rotation("aeiou", &mut rng), "aeiou");
}
