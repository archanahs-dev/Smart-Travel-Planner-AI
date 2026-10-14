from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue


def create_pdf(
    destination,
    weather,
    hotel,
    budget,
    itinerary,
    packing,
    reflection
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = darkblue

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    story = []

    # -----------------------
    # Title
    # -----------------------

    story.append(
        Paragraph(
            "Smart Travel Planner",
            title
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Destination :</b> {destination}",
            normal
        )
    )

    story.append(Spacer(1, 15))

    # -----------------------
    # Weather
    # -----------------------

    story.append(
        Paragraph(
            "Weather",
            heading
        )
    )

    story.append(
        Paragraph(
            f"Condition : {weather['Condition']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Temperature : {weather['Temperature']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Advice : {weather['Advice']}",
            normal
        )
    )

    story.append(Spacer(1, 15))

    # -----------------------
    # Hotel
    # -----------------------

    story.append(
        Paragraph(
            "Hotel",
            heading
        )
    )

    if hotel["Status"]:

        story.append(
            Paragraph(
                f"Hotel : {hotel['Hotel Name']}",
                normal
            )
        )

        story.append(
            Paragraph(
                f"Category : {hotel['Category']}",
                normal
            )
        )

        story.append(
            Paragraph(
                f"Price : {hotel['Price']}",
                normal
            )
        )

        story.append(
            Paragraph(
                f"Location : {hotel['Location']}",
                normal
            )
        )

        story.append(
            Paragraph(
                f"Rating : {hotel['Rating']}",
                normal
            )
        )

    else:

        story.append(
            Paragraph(
                hotel["Message"],
                normal
            )
        )

    story.append(Spacer(1, 15))
        # -----------------------
    # Budget
    # -----------------------

    story.append(
        Paragraph(
            "Budget",
            heading
        )
    )

    if budget["Status"]:

        story.append(Paragraph(f"Hotel Cost : {budget['Hotel Cost']}", normal))
        story.append(Paragraph(f"Food Cost : {budget['Food Cost']}", normal))
        story.append(Paragraph(f"Transport Cost : {budget['Transport Cost']}", normal))
        story.append(Paragraph(f"Activities Cost : {budget['Activities Cost']}", normal))
        story.append(Paragraph(f"<b>Total Budget : {budget['Total Budget']}</b>", normal))
        story.append(Paragraph(f"Trip Type : {budget['Trip Type']}", normal))

    story.append(Spacer(1, 15))

    # -----------------------
    # Itinerary
    # -----------------------

    story.append(
        Paragraph(
            "Daily Itinerary",
            heading
        )
    )

    for day in itinerary:

        story.append(
            Paragraph(
                f"<b>Day {day['Day']}</b>",
                normal
            )
        )

        story.append(Paragraph(f"Morning : {day['Morning']}", normal))
        story.append(Paragraph(f"Afternoon : {day['Afternoon']}", normal))
        story.append(Paragraph(f"Evening : {day['Evening']}", normal))
        story.append(Paragraph(f"Food : {day['Food']}", normal))
        story.append(Paragraph(f"Tip : {day['Tip']}", normal))
        story.append(Spacer(1, 10))

    # -----------------------
    # Packing List
    # -----------------------

    story.append(
        Paragraph(
            "Packing Checklist",
            heading
        )
    )

    for item in packing:
        story.append(Paragraph(f"• {item}", normal))

    story.append(Spacer(1, 15))

    # -----------------------
    # AI Suggestions
    # -----------------------

    story.append(
        Paragraph(
            "AI Suggestions",
            heading
        )
    )

    for tip in reflection:
        story.append(Paragraph(f"• {tip}", normal))

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf