      // ---- animated rain ---------------------------------------------------
      // Tuning lives here: density multiplies how much falls, speed multiplies
      // how fast. Raise density for a downpour, drop it for a fine mist.
      Item {
        id: rainLayer
        anchors.fill: parent

        property real density: 1.0
        property real speed: 1.0

        visible: opacity > 0
        opacity: root.raining ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: 1600; easing.type: Easing.InOutQuad } }

        ParticleSystem {
          id: rainSystem
          anchors.fill: parent
          // Fully stopped when dry, so a clear wallpaper costs nothing.
          running: rainLayer.opacity > 0
        }

        // The drizzle itself: fine, short, slow, barely any wind.
        Emitter {
          system: rainSystem
          group: "far"
          x: -parent.width * 0.2
          y: -100
          width: parent.width * 1.4
          height: 20
          emitRate: Math.round(620 * rainLayer.density)
          lifeSpan: Math.round(5400 / rainLayer.speed)
          lifeSpanVariation: 900
          size: 30
          sizeVariation: 12
          velocity: AngleDirection {
            angle: 93; angleVariation: 2.5
            magnitude: 250 * rainLayer.speed
            magnitudeVariation: 70 * rainLayer.speed
          }
        }

        ImageParticle {
          system: rainSystem
          groups: ["far"]
          source: "assets/raindrop.png"
          color: "#cfe6ff"
          colorVariation: 0.06
          alpha: 0.0
          opacity: 0.20
          autoRotation: true
          entryEffect: ImageParticle.Fade
        }

        // A few nearer drops, fatter and quicker, for depth.
        Emitter {
          system: rainSystem
          group: "near"
          x: -parent.width * 0.2
          y: -180
          width: parent.width * 1.4
          height: 20
          emitRate: Math.round(22 * rainLayer.density)
          lifeSpan: Math.round(4000 / rainLayer.speed)
          lifeSpanVariation: 800
          size: 62
          sizeVariation: 24
          velocity: AngleDirection {
            angle: 94; angleVariation: 3
            magnitude: 480 * rainLayer.speed
            magnitudeVariation: 130 * rainLayer.speed
          }
        }

        ImageParticle {
          system: rainSystem
          groups: ["near"]
          source: "assets/raindrop-near.png"
          color: "#eaf4ff"
          colorVariation: 0.04
          alpha: 0.0
          opacity: 0.12
          autoRotation: true
          entryEffect: ImageParticle.Fade
        }
      }
