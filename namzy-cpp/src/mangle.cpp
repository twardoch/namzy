// this_file: namzy-cpp/src/mangle.cpp
#include "mangle.h"
#include "wordlist.h"
#include <QVector>

namespace {
constexpr int kMaxLen = 12;
constexpr int kMaxTries = 8;

bool hasTripleLetter(const QString& s) {
    for (int i = 2; i < s.size(); ++i) {
        if (s.at(i) == s.at(i - 1) && s.at(i) == s.at(i - 2)) return true;
    }
    return false;
}

bool junctionUgly(const QString& compound, int junction) {
    const int start = std::max(0, junction - 2);
    const int end = std::min(compound.size(), junction + 2);
    const QString win = compound.mid(start, end - start);
    for (const QString& seam : namzy::badSeams()) {
        if (win.contains(seam)) return true;
    }
    return false;
}

QString capitalize(const QString& s) {
    if (s.isEmpty()) return s;
    return QString(s.at(0).toUpper()) + s.mid(1);
}
} // namespace

QString applyRotation(const QString& s, QRandomGenerator& rng) {
    struct Match { int i; QString src; QString dst; };
    QVector<Match> matches;
    const auto& rules = namzy::rotations();
    for (int i = 0; i < s.size(); ++i) {
        for (const auto& r : rules) {
            const QString& src = r.first;
            if (i + src.size() <= s.size() && s.mid(i, src.size()) == src) {
                matches.append(Match{ i, src, r.second });
            }
        }
    }
    if (matches.isEmpty()) return s;
    const Match& m = matches.at(static_cast<int>(rng.bounded(static_cast<quint32>(matches.size()))));
    return s.left(m.i) + m.dst + s.mid(m.i + m.src.size());
}

QString buildName(QRandomGenerator& rng) {
    const QStringList& stems = namzy::stems();
    const int n = stems.size();
    QString best;
    for (int t = 0; t < kMaxTries; ++t) {
        const QString a = stems.at(static_cast<int>(rng.bounded(static_cast<quint32>(n))));
        const QString b = stems.at(static_cast<int>(rng.bounded(static_cast<quint32>(n))));
        const QString compound = a + b;
        if (compound.size() > kMaxLen || hasTripleLetter(compound) || junctionUgly(compound, a.size())) {
            if (best.isEmpty()) best = compound;
            continue;
        }
        return capitalize(applyRotation(compound, rng));
    }
    return capitalize(applyRotation(best, rng));
}
